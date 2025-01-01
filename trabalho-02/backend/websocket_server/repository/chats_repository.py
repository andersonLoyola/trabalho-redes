from bson import ObjectId

class ChatsRepository(): 

    def __init__(self, db):
       self.collection = db['chats']
    

    def get_chat_participants(self, chat_id):
        return self.collection.find_one({ '_id': ObjectId(chat_id) }, { '_id': 1, 'users': 1 })