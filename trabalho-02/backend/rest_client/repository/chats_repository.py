import uuid
class ChatsRepository():
    def __init__(self, conn):
        self.conn = conn 

    def create_chat(self, chat_name, user_id, chat_type):
        chat_id = str(uuid.uuid4())
        chat_user_id = str(uuid.uuid4())
        create_chat_query = """
            INSERT INTO chats(
                id,
                name,
                chat_type
            )
            VALUES (?,?,?)
        """ 
        create_chat_users_query = """
            INSERT INTO chat_users (
                id,
                user_id,
                chat_id
            ) VALUES (?,?,?)
        """
        cursor = self.conn.cursor()
        cursor.execute("BEGIN;")
        try:
            cursor.execute(create_chat_query, (chat_id, chat_name, chat_type))
            cursor.execute(create_chat_users_query, (chat_user_id, user_id, chat_id))
            cursor.execute("COMMIT;")
            return str(chat_id) 
        except Exception as e:
            cursor.execute("ROLLBACK;")
            print(e)
            raise e

    # def get_chat_details(self, chat_id): #TODO: maybe change this to get chat by user later
    #     return self.collection.find_one({
    #         "_id": ObjectId(chat_id)
    #     }) 

    # def add_user(self, user_id, chat_id):
    #     return self.collection.update_one({
    #         {
    #             "_id": ObjectId(chat_id)
    #         },
    #         {
    #             "$addToSet": {
    #                 "users": user_id,
    #             }
    #         }
    #     })
    
    # def add_users(self, chat_id, users):
    #     return self.collection.update_one(
    #         {
    #             "_id": ObjectId(chat_id)
    #         },
    #         {
    #             "$addToSet": {
    #                 "users": {
    #                     "$each": users
    #                 }
    #             }
    #         }
    #     )
    
    # def get_user_chats(self, user_id):
    #     return self.collection.find({
    #         "users": {
    #             "$in": [user_id]
    #         }
    #     })
       

    # def remove_user(self, user_id, chat_id):
    #     return self.collection.update_one({
    #         {
    #             "_id": ObjectId(chat_id)
    #         },
    #         {
    #             "$pull": {
    #                 "users": user_id,
    #             }
    #         }
    #     })
    