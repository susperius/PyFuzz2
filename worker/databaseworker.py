__author__ = 'susperius'

import sqlite3 as sql
import gevent
from worker import Worker
from model.crash import Crash
from model.node import PyFuzz2Node

DB_TYPES = {'CRASH': 0x01, 'NODE': 0x02}
SEPARATOR = "_;_"


class DatabaseWorker(Worker):
    def __init__(self, db_queue, node_dict=None, crash_dict=None):
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
        self._cursor.execute("SELECT * FROM crashes WHERE program_maj_hash=? LIMIT 1", key)
        result = self._cursor.fetchall()
        return True if len(result) > 0 else False

    def node_exists(self, address):
        self._cursor.execute("SELECT * FROM nodes WHERE address=? LIMIT 1", address)
        result = self._cursor.fetchall()
        return True if len(result) > 0 else False

    def load(self):
        self._cursor.execute("SELECT address, name, listener_port, status, crashes, config FROM nodes")
        result = self._cursor.fetchall()
        if len(result) > 0:
            for row in result:
                self._node_dict[row[0]] = PyFuzz2Node(row[1], row[0], row[2])
                self._node_dict[row[0]].status = row[3]
                self._node_dict[row[0]].config = row[5]
        self._cursor.execute("SELECT program_maj_hash, min_hash, description, classification, "
                             "count, node_addr FROM crashes")
        result = self._cursor.fetchall()
        if len(result) > 0:
            for row in result:
                program, maj_hash = row[0].split(SEPARATOR)
                node_addresses = row[5].split(",")
                self._crash_dict[row[0]] = Crash(node_addresses[0], program, maj_hash, row[1], row[2], row[3], row[4])
                self._node_dict[node_addresses[0]].crashed(maj_hash)
                del(node_addresses[0])
                for addr in node_addresses:
                    self._node_dict[addr].crashed(maj_hash)
                    self._crash_dict[row[0]].add_node_address(addr)

    def __worker_green(self):
        while True:
            db_type, msg = self._db_queue.get()
            if db_type == DB_TYPES['CRASH']:
                key = self._crash_dict[msg].program + SEPARATOR + self._crash_dict[msg].major_hash
                if self.crash_exists(key):
                    data = [self._crash_dict[key].node_addr, self._crash_dict[key].count, key]
                    self._cursor.execute("UPDATE crashes SET node_addr=?, count=? WHERE program_maj_hash=?", data)
                else:
                    data = [key, self._crash_dict[key].minor_hash, self._crash_dict[key].short_description,
                            self._crash_dict[key].classification, self._crash_dict[key].count,
                            self._crash_dict[key].node_addresses]
                    self._cursor.execute("INSERT INTO crashes "
                                         "(program_maj_hash, min_hash, description, classification, count, node_addr)"
                                         " VALUES (?, ?, ?, ?, ?, ?)", data)
            elif db_type == DB_TYPES['NODE']:
                pass



