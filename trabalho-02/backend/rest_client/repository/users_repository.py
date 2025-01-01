from bson import ObjectId
class UsersRepository():
    def __init__(self, db):
        self.collection = db['users']

    def _map_users_info(self, users_cursor):
        return [{"username": user['username'], "_id": str(user['_id'])} for user in list(users_cursor)]

    def get_user(self, username):
        return self.collection.find_one({"username": username})
    
    def get_users_by_ids(self, user_ids):
        users_cursor =  self.collection.find(
            {
                "_id": {
                    "$in": [ObjectId(user_id) for user_id in user_ids]
                }
            }, {"username": 1, "_id": 1}
        )

        return self._map_users_info(users_cursor)

    def create_user(self, user):
        return self.collection.insert_one({"username": user['username'], "password": user['password']})

    def delete_user(self, user_id):
        return self.collection.delete_one(user_id)