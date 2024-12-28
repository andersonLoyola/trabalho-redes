class UsersRepository():
    def __init__(self, db):
        self.collection = db['users']

    def get_user(self, username):
        return self.collection.find_one({"username": username})

    def create_user(self, user):
        return self.collection.insert_one({"username": user['username'], "password": user['password']})

    def delete_user(self, user_id):
        return self.collection.delete_one(user_id)