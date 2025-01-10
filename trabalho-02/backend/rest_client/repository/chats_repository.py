import uuid

class ChatsRepository(): 

    def __init__(self, connection_pool):
        self.connection_pool = connection_pool
        
    def create_chat(self, user_id, chat_name):
        conn = self.connection_pool.get_connection()
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
            print(f'create_chat: {e}')
            raise e
        finally:
            self.connection_pool.release_connection(conn)

    def get_chats_info(self):
        conn = self.connection_pool.get_connection()
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
        """
        try:
            result = cursor.execute(get_user_chats_query)
            return result.fetchall()
        except Exception as e:
            print(f'get_chats_info: {e}')
            raise e
        finally:
            self.connection_pool.release_connection(conn)
        

    def get_chat_participant(self, user_id, chat_id):
        conn = self.connection_pool.get_connection()
        cursor = conn.cursor()
        get_chat_participant = """
            SELECT 
                u.id as user_id,
                u.username as user_name,
                cu.chat_id as chat_id
            FROM    
                chat_users cu
            INNER JOIN users u
            ON cu.user_id = cu.user_id
            WHERE 
                cu.user_id = ?
                AND cu.chat_id = ?
        """ 
        try:
            found_chat_connection = cursor.execute(get_chat_participant, (user_id, chat_id))
            return found_chat_connection.fetchone()
        except Exception as e:
            print(f'get_chat_participant: {e}')
            raise e
        finally:
            self.connection_pool.release_connection(conn)

    def get_chat_participants(self, chat_id):
        conn = self.connection_pool.get_connection()
        cursor = conn.cursor()
        query = """
            SELECT   
                u.id as user_id,
                u.username as user_name,
                cu.chat_id as chat_id
            FROM 
                chat_users cu
            INNER JOIN users u
            ON cu.user_id = cu.user_id
            WHERE 
                cu.chat_id = ?
        """
        try: 
            cursor.execute(query, (chat_id,))
            chat_particants = cursor.fetchall()
            return chat_particants
        except Exception as e:
            print(f'get_chat_participants: {e}')
            raise e
        finally:
            self.connection_pool.release_connection(conn)
    
 
    def get_chat_by_name(self, chat_name):
        conn = self.connection_pool.get_connection()
        cursor = conn.cursor()
        query = """
            SELECT   
                c.name as chat_name,
                c.id as chat_id
            FROM 
               chats c
            WHERE 
                c.name = ?
        """
        try: 
            cursor.execute(query, (chat_name,))
            found_chat = cursor.fetchone()
            return found_chat
        except Exception as e:
            print(f'get_chat_participants: {e}')
            raise e
        finally:
            self.connection_pool.release_connection(conn)
    
  
    def get_chat_by_id(self, chat_id):
        conn = self.connection_pool.get_connection()
        cursor = conn.cursor()
        query = """
            SELECT   
                c.name as chat_name,
                c.id as chat_id
            FROM 
               chats c
            WHERE 
                c.id = ?
        """
        try: 
            cursor.execute(query, (chat_id,))
            found_chat = cursor.fetchone()
            return found_chat
        except Exception as e:
            print(f'get_chat_participants: {e}')
            raise e
        finally:
            self.connection_pool.release_connection(conn)
    
    def add_chat_participant(self, chat_id, user_id):
        conn = self.connection_pool.get_connection()
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
            print(f'add_chat_participant: {e}')
            raise e
        finally:
            self.connection_pool.release_connection(conn)
    
    # def get_chat_details(self, chat_id):
    #     # conn = self.connection_pool.get_connection()
    #     # cursor = conn.cursor()
    #     # add_user_to_chat_info = """
    #     #     SELECT chat_users (
    #     #         chat_id,
    #     #         user_id
    #     #     ) VALUES (?, ?)
    #     # """
    #     try:
    #        pass
    #     except Exception as e:
    #         print(f'add_chat_participant: {e}')
    #         raise e
    #     finally:
    #         self.connection_pool.release_connection(conn)