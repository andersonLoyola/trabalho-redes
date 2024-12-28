import datetime

class MessagesRepository():

    def __init__(self, db):
        self.messages_collection = db['messages']

    def add_message(self, sender, receiver, message):
        message_document = {
            'sender': sender,
            'receiver': receiver,
            'message': message,
            'created_at': datetime.now()
        }
        self.messages_collection.insert(message_document)

    def get_messages(self, sender, receiver):
        return self.messages_collection.find({ 'sender': sender, 'receiver': receiver }).sort('created_at', 1)