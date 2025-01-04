import sqlite3
import datetime
from serializers import SqliteSerializer

class MessagesRepository():

    def __init__(self, db_path):
        self.messages_tb_name = 'messages'
        self.db__path = db_path

    def create_message(self, sender, receiver, message, attachment):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = SqliteSerializer().to_dict
        cursor = conn.cursor()
        query = """
            INSERT INTO ? (sender, receiver, message, attachment, created_at)
            VALUES (?, ?, ?, ?, ?)
        """
        cursor = conn.cursor()
        cursor.execute(query, (
            self.messages_tb_name, 
            sender, 
            receiver,
            message, 
            attachment, 
            datetime.datetime.now()
            )
        )
        conn.commit()
        conn.close()
