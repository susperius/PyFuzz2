__author__ = 'susperius'

import sqlite3 as sql
import gevent
import logging
import pickle
from worker import Worker
from model.crash import Crash
from model.pyfuzz2_node import PyFuzz2Node

DB_TYPES = {'CRASH': 0x01, 'NODE': 0x02}
SEPARATOR = "_;_"


class DatabaseWorker(Worker):
    def __init__(self, db_queue, node_dict=None, crash_dict=None):
        self._logger = logging.getLogger(__name__)
        self._db_queue = db_queue
        self._node_dict = node_dict if node_dict is not None else {}
        self._crash_dict = crash_dict if crash_dict is not None else {}
        self._db_conn = sql.connect("data/server.db")
        self._cursor = self._db_conn.cursor()
        self._greenlet = None

    @property
    def node_dict(self):
        return self._node_dict

    @property
    def crash_dict(self):
        return self._crash_dict

    def stop_worker(self):
        if self._greenlet is not None:
            gevent.kill(self._greenlet)
            self._greenlet = None
            self._db_conn.commit()
            self._db_conn.close()

    def start_worker(self):
        if self._greenlet is None:
            self._greenlet = gevent.spawn(self.__worker_green)
            gevent.sleep(0)

    def select_single_node(self, address):
        self._cursor.execute("SELECT address, name, listener_port, status, crashes, config FROM nodes WHERE address=? LIMIT 1",
                             address)
        return self._cursor.fetchone()

    def crash_exists(self, key):
        binding = [key]
        self._cursor.execute("SELECT * FROM crashes WHERE program_maj_hash=? LIMIT 1", binding)
        result = self._cursor.fetchall()
        return True if len(result) > 0 else False

    def node_exists(self, address):
        binding = [address]
        self._cursor.execute("SELECT * FROM nodes WHERE address=? LIMIT 1", binding)
        result = self._cursor.fetchall()
        return True if len(result) > 0 else False

    def load(self):
        self._cursor.execute("SELECT address, name, listener_port, status, crashes, config FROM nodes")
        result = self._cursor.fetchall()
        if len(result) > 0:
            for row in result:
                self._node_dict[row[0]] = PyFuzz2Node(row[1], row[0], row[2])
                self._node_dict[row[0]].status = bool(row[3])
                self._node_dict[row[0]].config = row[5]
        self._cursor.execute("SELECT program_maj_hash, min_hash, description, classification, "
                             "count, node_addr FROM crashes")
        result = self._cursor.fetchall()
        if len(result) > 0:
            for row in result:
                program, maj_hash = row[0].split(SEPARATOR)
                node_addresses = pickle.load(row[5])
                self._crash_dict[row[0]] = Crash(node_addresses, program, maj_hash, row[1], row[2], row[3], row[4])
                for addr in node_addresses:
                    self._node_dict[addr].crashed(maj_hash)

    def __worker_green(self):
        while True:
            db_type, msg = self._db_queue.get()
            if db_type == DB_TYPES['CRASH']:
                key = self._crash_dict[msg].program + SEPARATOR + self._crash_dict[msg].major_hash
                self._logger.debug("DB-Crash Access Key -> " + key)
                if self.crash_exists(key):
                    data = [pickle.dump(self._crash_dict[key].node_addresses), self._crash_dict[key].count, key]
                    self._cursor.execute("UPDATE crashes SET node_addr=?, count=? WHERE program_maj_hash=?", data)
                else:
                    data = [key, self._crash_dict[key].minor_hash, self._crash_dict[key].short_description,
                            self._crash_dict[key].classification, self._crash_dict[key].count,
                            pickle.dump(self._crash_dict[key].node_addresses)]
                    self._cursor.execute("INSERT INTO crashes "
                                         "(program_maj_hash, min_hash, description, classification, count, node_addr)"
                                         " VALUES (?, ?, ?, ?, ?, ?)", data)
            elif db_type == DB_TYPES['NODE']:
                key = msg
                self._logger.debug("DB-Node Access Key -> " + key)
                if self.node_exists(key):
                    data = [self._node_dict[key].name, self._node_dict[key].listener_port,
                            str(self._node_dict[key].status),
                            str(self._node_dict[key].crash_hashes), self._node_dict[key].config, key]
                    self._cursor.execute("UPDATE nodes SET name=?, listener_port=?, status=?, crashes=?, config=? "
                                         "WHERE address=?", data)
                else:
                    data = [key, self._node_dict[key].name, self._node_dict[key].listener_port,
                            str(self._node_dict[key].status),
                            str(self._node_dict[key].crash_hashes), self._node_dict[key].config]
                    self._cursor.execute("INSERT INTO nodes (address, name, listener_port, status, crashes, config) "
                                         "VALUES (?, ?, ?, ?, ?, ?)", data)
            self._db_conn.commit()



