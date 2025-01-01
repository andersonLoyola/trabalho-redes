class ChatsRepository(): 

    def __init__(self, db):
       self.chats_table_name = 'chats'
       self.db = db
    

    def get_chat_participants(self, chat_id):
        query = f"SELECT users from ? WHERE id = ?"
        cursor = self.db.cursor()
        cursor.execute(query, (self.chats_table_name, chat_id))
        chat_particants = cursor.fetchone()
        return chat_particants
    
    