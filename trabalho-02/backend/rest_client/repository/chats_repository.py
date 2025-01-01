from bson import ObjectId

class ChatsRepository():
    def __init__(self, db):
        self.collection = db['chats']

    def create_chat(self, chat_name, user_id, chat_type):
        chat_id =  self.collection.insert_one({
            "chat_type": chat_type,
            "chat_name": chat_name,
            "users": [user_id],
            "messages": [],
        }).inserted_id
        
        return str(chat_id)

    def get_chat_details(self, chat_id): #TODO: maybe change this to get chat by user later
        return self.collection.find_one({
            "_id": ObjectId(chat_id)
        }) 

    def add_user(self, user_id, chat_id):
        return self.collection.update_one({
            {
                "_id": ObjectId(chat_id)
            },
            {
                "$addToSet": {
                    "users": user_id,
                }
            }
        })
    
    def add_users(self, chat_id, users):
        return self.collection.update_one(
            {
                "_id": ObjectId(chat_id)
            },
            {
                "$addToSet": {
                    "users": {
                        "$each": users
                    }
                }
            }
        )
    
    def get_user_chats(self, user_id):
        return self.collection.find({
            "users": {
                "$in": [user_id]
            }
        })
       

    def remove_user(self, user_id, chat_id):
        return self.collection.update_one({
            {
                "_id": ObjectId(chat_id)
            },
            {
                "$pull": {
                    "users": user_id,
                }
            }
        })
    