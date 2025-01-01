from bson import ObjectId

class MessagesRepository:
    def __init__(self, db):
        self.collection = db['messages']

    def get_messages_by_ids(self, message_ids): 
        
        messages_cursor = self.collection.find({
            "_id": {
                "$in": [ObjectId(message_id) for message_id in message_ids]
            }
        })

        return messages_cursor