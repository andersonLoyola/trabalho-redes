import datetime

class UserConnectionsRepository():

    def __init__(self, db):
        self.user_connection_collections = db['user_connections']

    def get_user_connections(self, user_id):
        
        query = {
            'user_id': user_id
        }

        return self.user_connection_collections.find(query)

    def add_user_connection(self, user_id, connection_id, connection_type):
        connection_document = {
            'user_id': user_id,
            'connection_id': connection_id,
            'connection_type': connection_type,
            'created_at': datetime.now()
        }
        self.user_connection_collections.insert(connection_document)

    def remove_user_connection(self, user_id, connection_id):
        query = {
            'user_id': user_id,
            'connection_id': connection_id
        }
        self.user_connection_collections.remove(query)