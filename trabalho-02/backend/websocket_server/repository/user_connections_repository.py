import datetime

class UserConnectionsRepository():

    def __init__(self, db):
        self.user_connection_collections = db['user_connections']

    def get_user_connections(self, user_id):
        query = {
            'user_id': user_id,
            'status': 'active',
        }
        return self.user_connection_collections.count(query)

    def add_user_connection(self, user_id, connection_id):
        self.user_connection_collections.update_one({
            'user_id': user_id,
            'connection_id': connection_id
        }, { 
                '$set': { 
                    'status': 'active',
                    'created_at': datetime.datetime.now(), 
                    'updated_at': datetime.datetime.now() 
                }     
            }, upsert=True)
        

    def remove_user_connection(self, user_id, connection_id):
        self.user_connection_collections.update_one({
            'user_id': user_id,
            'connection_id': connection_id
        }, { '$set': { 'status': 'inactive', 'updated_at': datetime.datetime.now() } })