class ChatsRepository(): 

    def __init__(self, connection_pool):
        self.connection_pool = connection_pool
        
    def create_chat(self, chat_id, session_id, chat_name):
        conn = self.connection_pool.get_connection()
        cursor = conn.cursor()
        create_chat_query = """
            INSERT INTO chats(
                id,
                name
            )
            VALUES (?,?)
        """ 
        create_chat_users_query = """
            INSERT INTO chat_users (
                chat_id,
                user_session_id
            ) VALUES (?,?)
        """
        try:
            cursor.execute('BEGIN;')
            cursor.execute(create_chat_query, (chat_id, chat_name))
            cursor.execute(create_chat_users_query, (chat_id, session_id))
            conn.commit()
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
            WITH chat_subscribers AS (
                SELECT
                    cu.chat_id,
                    json_group_array(
                        json_object(
                            'session_id', us.session_id,
                            'user_id', us.user_id
                        )
                    ) as subscribers
                FROM chat_users cu
                INNER JOIN user_sessions us
                    ON us.session_id = cu.user_session_id
                GROUP BY cu.chat_id
            )
            SELECT 
                c.id as chat_id,
                c.name as chat_name,
                cs.subscribers
            FROM chats c
            LEFT JOIN chat_subscribers cs
                ON c.id = cs.chat_id
        """
        try:
            result = cursor.execute(get_user_chats_query)
            return result.fetchall()
        except Exception as e:
            print(f'get_chats_info: {e}')
            raise e
        finally:
            self.connection_pool.release_connection(conn)
        
    def get_chat_participant(self, chat_id, session_id):
        conn = self.connection_pool.get_connection()
        cursor = conn.cursor()
        get_chat_participant = """
            SELECT 
                cu.user_session_id,
                cu.chat_id
            FROM    
                chat_users cu
            WHERE 
                cu.user_session_id = ?
                AND cu.chat_id = ?
        """ 
        try:
            found_chat_connection = cursor.execute(get_chat_participant, (session_id, chat_id))
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
                us.session_id as session_id
                cu.chat_id as chat_id
            FROM 
                chat_users cu
            INNER JOIN user_sessions us
                ON us.session_id = cu.user_session_id
            INNER JOIN users u
                ON cu.user_id = us.user_id
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
    
    def add_chat_participant(self, chat_id, user_session_id):
        add_user_to_chat_query = """
            INSERT INTO chat_users (
                chat_id,
                user_session_id
            ) VALUES (?, ?)
        """
        try:
            conn = self.connection_pool.get_connection()
            cursor = conn.cursor()
            cursor.execute(add_user_to_chat_query, (chat_id, user_session_id))
            conn.commit()
        except Exception as e:
            print(f'add_chat_participant: {e}')
            raise e
        finally:
            self.connection_pool.release_connection(conn)
    
    def remove_chat_participant(self, chat_id, user_session_id):
        remove_user_from_chat_query = """
            DELETE FROM chat_users  
            WHERE 
                chat_users.user_session_id = ?
                AND chat_users.chat_id = ?
        """
        try:
            conn = self.connection_pool.get_connection()
            cursor = conn.cursor()
            cursor.execute(remove_user_from_chat_query, (chat_id, user_session_id))
            conn.commit()
        except Exception as e:
            print(f'add_chat_participant: {e}')
            raise e
        finally:
            self.connection_pool.release_connection(conn)
    
    def get_user_chats(self, user_id):
        get_user_chats_query = """
            SELECT 
                c.id as chat_id,
                c.chat_name
            FROM users u
            INNER JOIN user_sessions us
                ON u.user_id = u.id
            INNER JOIN chat_users cu
                ON cu.user_session_id = us.session_id
            INNER JOIN chats c
                ON c.id = cu.chat_id
            WHERE u.id = ?
        """
        try:
            conn = self.connection_pool.get_connection()
            cursor = conn.cursor()
            cursor.execute(get_user_chats_query, (user_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f'get_user_chats: {e}')
            raise e
        finally:
            self.connection_pool.release_connection(conn)