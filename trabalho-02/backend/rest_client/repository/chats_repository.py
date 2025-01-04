import uuid
class ChatsRepository():
    def __init__(self, conn):
        self.conn = conn 

    def create_chat(self, chat_name, user_id):
        chat_id = str(uuid.uuid4())
        create_chat_query = """
            INSERT INTO chats(
                id,
                name,
            )
            VALUES (?, ?)
        """ 
        create_chat_users_query = """
            INSERT INTO chat_users (
                user_id,
                chat_id
            ) VALUES (?,?)
        """
        cursor = self.conn.cursor()
        cursor.execute("BEGIN;")
        try:
            cursor.execute(create_chat_query, (chat_id, chat_name))
            cursor.execute(create_chat_users_query, (user_id, chat_id))
            cursor.execute("COMMIT;")
            return str(chat_id) 
        except Exception as e:
            cursor.execute("ROLLBACK;")
            print(e)
            raise e

    def get_chat_details(self, chat_id): #TODO: maybe change this to get chat by user later
        cursor=self.conn.cursor()
        get_chat_users_info = """
           SELECT 
                u.id as user_id,
                u.username
            FROM chats c
            INNER JOIN chat_users cu
            ON cu.chat_id = c.id
            INNER JOIN users u
            ON u.id  = cu.user_id 
            WHERE c.id = ?
        """
        get_chat_messages_query = """
            SELECT 
                (
                    SELECT 
                        u.username
                    FROM users u 
                    INNER JOIN chat_messages cm
                    ON cm.user_id = u.id
                    WHERE cm.message_id = m.id
                ) as sender
            FROM messages m
            WHERE m.id = ?
        """

        try:
            result = cursor.execute(get_user_chats_query, (user_id,))
            return result.fetchall()
        except Exception as e:
            cursor.execute("ROLLBACK;")
            print(e)
            raise e

    def get_user_chats(self, user_id):
        get_user_chats_query = """
            SELECT 
                c.id as chat_id,
                c.name as chat_name,
                c.type as chat_type
            FROM chat_users cu
            INNER JOIN chats c
            ON cu.chat_id = c.id
            WHERE cu.user_id = ?
        """

        cursor = self.conn.cursor()
       
        try:
            result = cursor.execute(get_user_chats_query, (user_id,))
            return result.fetchall()
        except Exception as e:
            cursor.execute("ROLLBACK;")
            print(e)
            raise e

    