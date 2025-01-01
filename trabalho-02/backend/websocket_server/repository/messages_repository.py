import datetime

class MessagesRepository():

    def __init__(self, db):
        self.messages_tb_name = 'messages'
        self.db = db

    def create_message(self, sender, receiver, message, attachment):
        query = """
            INSERT INTO ? (sender, receiver, message, attachment, created_at)
            VALUES (?, ?, ?, ?, ?)
        """
        cursor = self.db.cursor()
        cursor.execute(query, (
            self.messages_tb_name, 
            sender, 
            receiver,
            message, 
            attachment, 
            datetime.datetime.now()
            )
        )
        self.db.commit()
