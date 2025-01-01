import uuid 

class UsersRepository:
    def __init__(self, db):
        self.db = db
        self.user_table_name = 'users'

    def create_user(self, username, password):
        user_id = uuid.uuid4()
        query = """
            INSERT INTO ? (
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
        cursor = self.db.cursor()
        cursor.execute(query, (self.user_table_name, user_id, username, password))
        self.db.commit()

    def get_user(self, username):
        query  = f"""
            SELECT * 
            FROM {self.user_table_name}
            WHERE username = ?
        """
        cursor = self.db.cursor()
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        return user