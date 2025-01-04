import uuid
import sqlite3
from serializers import SqliteSerializer
class UsersRepository:
    def __init__(self, db_path):
        self.db_path = db_path

    def create_user(self, username, password):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = SqliteSerializer().to_dict
        cursor = conn.cursor()
        user_id = str(uuid.uuid4())
        query = """
            INSERT INTO users (
                id,
                username,
                password 
            )
            VALUES (
                ?,
                ?,
                ?
            )
        """
        cursor = conn.cursor()
        cursor.execute(query, (user_id, username, password))
        conn.commit()

    def get_user(self, username):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = SqliteSerializer().to_dict
        cursor = conn.cursor()
        query  = f"""
            SELECT * 
            FROM users
            WHERE username = ?
        """
        cursor = conn.cursor()
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        conn.close()
        return user