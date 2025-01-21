import sqlite3
import threading
from queue import Queue
from serializers import SqliteSerializer

class ConnectionPool:
    def __init__(self, db_path, pool_size=5):
        self.db_path = db_path
        self.pool_size = pool_size
        self.pool = Queue(maxsize=pool_size)
        self._lock = threading.Lock()
        for _ in range(pool_size):
            conn = sqlite3.connect(db_path, check_same_thread=False, timeout=15.0) # Waits at most 15 seconds for transaction end
            conn.row_factory = SqliteSerializer.to_dict
            conn.execute('PRAGMA journal_mode=WAL')
            conn.execute('pragma busy_timeout=500;')
            self.pool.put(conn)

    def get_connection(self):
        with self._lock:
            return self.pool.get()

    def release_connection(self, conn):
        with self._lock:
            self.pool.put(conn)

    def close_all_connections(self):
        while not self.pool.empty():
            conn = self.pool.get()
            conn.close()