import datetime

class MessagesRepository():

    def __init__(self, db):
        self.collection = db['messages']

    def create_message(self, sender, receiver, message, attachment):
        message_document = {
            'sender': sender,
            'receiver': receiver,
            'message': message,
            'attachment': attachment,
            'created_at': datetime.datetime.now()
        }
        result = self.collection.insert_one(message_document)
   