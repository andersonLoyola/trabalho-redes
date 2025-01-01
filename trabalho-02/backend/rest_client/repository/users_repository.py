import uuid
class UsersRepository():
    def __init__(self, conn):
        self.user_table_table = 'users'
        self.conn = conn

 
    def get_user(self, username):
        cursor = self.conn.cursor()
        query = """
            SELECT * FROM users u
            WHERE u.username = :username
        """
        result = cursor.execute(query, (username,))
        return result.fetchone()

    
    def get_users_by_ids(self, user_ids):
        masked_ids = [ '?' for (_) in user_ids]
        cursor = self.conn.cursor()
        query = f"""
            SELECT 
                id,
                username
            FROM users u
            WHERE 
                id IN  ({masked_ids.keys().join(',')})
        """
        results = cursor.execute(query, list(user_ids))
        return results.fetchmany()

    def create_user(self, user):
        id = uuid.uuid4()
        cursor = self.conn.cursor()
        query = f""" 
            INSERT INTO users
            VALUES (?, ?, ?)
        """
        cursor.execute(query,(str(id), user['username'], user['password']))
        self.conn.commit()
        