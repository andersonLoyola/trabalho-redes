import uuid
import datetime

class UsersRepository:
    def __init__(self, connection_pool):
        self.connection_pool = connection_pool

    def create_user(self, user_data):
        username = user_data['username']
        password = user_data['password']
        try:
            conn = self.connection_pool.get_connection()
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
            cursor.execute(query, (user_id, username, password))
            conn.commit()
        except Exception as e:
            print(f'create_user: {e}')
            raise e
        finally:
            self.connection_pool.release_connection(conn)
    
    def get_user(self, username):
        try:
            conn = self.connection_pool.get_connection()
            cursor = conn.cursor()
            query  = f"""
                SELECT * 
                FROM users
                WHERE username = ?
            """
            cursor = conn.cursor()
            cursor.execute(query, (username,))
            user = cursor.fetchone()
            return user
        except Exception as e:
            print(f'get_user: {e}')
            raise e
        finally:
            self.connection_pool.release_connection(conn)
    
    def create_user_session(self, user_id, session_id):
        try:
            conn = self.connection_pool.get_connection()
            cursor = conn.cursor()
            query  = """
                INSERT INTO user_sessions(
                    user_id,
                    session_id
                ) VALUES  (
                    ?,
                    ?
                )
            """
            cursor = conn.cursor()
            cursor.execute(query, (user_id, session_id))
            conn.commit()
            return session_id
        except Exception as e:
            print(f'create_user_session: {e}')
            raise e
        finally:
            self.connection_pool.release_connection(conn)
    
    def update_user_session_status(self, user_id, session_id, status):
        try:
            current_time = datetime.datetime.now()
            conn = self.connection_pool.get_connection()
            cursor = conn.cursor()
            query = """
                UPDATE user_sessions 
                    SET 
                        status = ?,
                        updated_at = ?
                WHERE 
                    session_id = ?
                    AND user_id = ? 
            """
            cursor = conn.cursor()
            cursor.execute(query, (status, current_time, session_id, user_id))
            conn.commit()
        except Exception as e:
            print(f'update_user_session_status: {e}')
            raise e
        finally:
            self.connection_pool.release_connection(conn)
    
    def count_user_sessions(self, user_id):
        try:
            conn = self.connection_pool.get_connection()
            cursor = conn.cursor()
            query  = """
                SELECT 
                    count(us.session_id)  as sessions_count
                FROM 
                    user_sessions us
                WHERE
                    us.user_id = ?       
            """
            cursor = conn.cursor()
            cursor.execute(query, (user_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f'count_user_sessions: {e}')
            raise e
        finally:
            self.connection_pool.release_connection(conn)
   
    def find_inactive_sessions(self, user_id):
        try:
            conn = self.connection_pool.get_connection()
            cursor = conn.cursor()
            query  = """
                SELECT 
                    us.session_id,
                    us.user_id
                FROM 
                    user_sessions us
                WHERE
                    us.user_id = ?
                    AND us.status = 'INACTIVE'       
            """
            cursor = conn.cursor()
            cursor.execute(query, (user_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f'find_inactive_sessions: {e}')
            raise e
        finally:
            self.connection_pool.release_connection(conn)
    
    def find_user_by_session_id(self, session_id):
        try:
            conn = self.connection_pool.get_connection()
            cursor = conn.cursor()
            query  = """
                SELECT 
                    u.id as user_id,
                    u.username as user_name,
                    us.session_id as session_id
                FROM 
                    user_sessions us
                    INNER JOIN users u
                    ON u.id = us.user_id
                WHERE
                    us.session_id = ?      
            """
            cursor = conn.cursor()
            cursor.execute(query, (session_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f'find_user_by_session_id: {e}')
            raise e
        finally:
            self.connection_pool.release_connection(conn)
            
   
    def find_user_sessions(self, user_id):
        try:
            conn = self.connection_pool.get_connection()
            cursor = conn.cursor()
            query  = """
                SELECT 
                    us.session_id as session_id
                FROM 
                    user_sessions us
                  
                WHERE
                    us.user_id = ?      
            """
            cursor = conn.cursor()
            cursor.execute(query, (user_id,))
            found_sessions = cursor.fetchall()
            return [session['session_id'] for session in found_sessions]
        except Exception as e:
            print(f'find_user_sessions: {e}')
            raise e
        finally:
            self.connection_pool.release_connection(conn)
