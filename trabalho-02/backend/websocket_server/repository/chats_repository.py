import uuid
import sqlite3
from serializers import SqliteSerializer
class ChatsRepository(): 

    def __init__(self, db_path):
       self.chats_table_name = 'chats'
       self.db_path = db_path
    

    def create_chat(self, user_id, chat_name):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = SqliteSerializer().to_dict
        cursor = conn.cursor()
        chat_id = str(uuid.uuid4())
        create_chat_query = """
            INSERT INTO chats(
                id,
                name
            )
            VALUES (?,?)
        """ 
        create_chat_users_query = """
            INSERT INTO chat_users (
                user_id,
                chat_id
            ) VALUES (?,?)
        """
        try:
            cursor.execute("BEGIN;")
            cursor.execute(create_chat_query, (chat_id, chat_name))
            cursor.execute(create_chat_users_query, (user_id, chat_id))
            cursor.execute("COMMIT;")
            return str(chat_id) 
        except Exception as e:
            cursor.execute("ROLLBACK;")
            print(e)
            raise e

    def get_chats_info(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = SqliteSerializer().to_dict
        cursor = conn.cursor()
        get_user_chats_query = """
            SELECT 
                c.id as chat_id,
                c.name as chat_name,
                 (
                    SELECT GROUP_CONCAT(cu.user_id)
                    FROM chat_users cu
                    WHERE cu.chat_id = c.id
                   
                ) as subscribers
            FROM chats c
            
            WHERE c.TYPE = 'GROUP'
        """
        try:
            result = cursor.execute(get_user_chats_query)
            return result.fetchall()
        except Exception as e:
            print(e)
            raise e


    def get_chat_participants(self, chat_id):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = SqliteSerializer().to_dict
        cursor = conn.cursor()
        query = f"SELECT users from ? WHERE id = ?"
        cursor = conn.cursor()
        cursor.execute(query, (self.chats_table_name, chat_id))
        chat_particants = cursor.fetchone()
        conn.close()
        return chat_particants
    
    def add_chat_participant(self, chat_id, user_id):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = SqliteSerializer().to_dict
        cursor = conn.cursor()
        add_user_to_chat_info = """
            INSERT INTO chat_users (
                chat_id,
                user_id
            ) VALUES (?, ?)
        """
        try:
            cursor.execute('BEGIN;')
            cursor.execute(add_user_to_chat_info, (chat_id, user_id))
            cursor.execute('COMMIT;')
        except Exception as e:
            print(e)
            raise e
    