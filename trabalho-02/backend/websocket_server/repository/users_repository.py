import uuid

class UsersRepository:
    def __init__(self, connection_pool):
        self.connection_pool = connection_pool

    def create_user(self, username, password):
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