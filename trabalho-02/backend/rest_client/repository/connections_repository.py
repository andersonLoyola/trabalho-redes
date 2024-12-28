class ConnectionsRepository():
    def __init__(self, db):
        self.collection = db['connections']

    def create_group_connection(self, connection_data):
        self.collection.insert(connection_data)

    def get_connections(self, user_id):
        return self.collection.find_all({"user_id": user_id})