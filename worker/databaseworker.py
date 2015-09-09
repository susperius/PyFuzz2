__author__ = 'susperius'

import sqlite3 as sql
import gevent
from worker import Worker
from model.crash import Crash
from model.node import PyFuzz2Node

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

    def start_worker(self):
        if self._greenlet is None:
            self._greenlet = gevent.spawn(self.__worker_green)
            gevent.sleep(0)

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
                program, maj_hash = row[0].split("_")
                node_addresses = row[5].split(",")
                self._crash_dict[row[0]] = Crash(node_addresses[0], program, maj_hash, row[1], row[2], row[3], row[4])
                self._node_dict[node_addresses[0]].crashed(maj_hash)
                del(node_addresses[0])
                for addr in node_addresses:
                    self._node_dict[addr].crashed(maj_hash)
                    self._crash_dict[row[0]].add_node_address(addr)

    def __worker_green(self):
        pass


