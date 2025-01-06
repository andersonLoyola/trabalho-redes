class ConnectionsService: 
    instance = None
    
    def __init__(self, chats_repository, db_persistance = False):
        self.MAX_CONNECTIONS = 50
        self.db_persistance = db_persistance
        self.chats_repository = chats_repository

    @classmethod
    def get_instance(cls, chat_repository):
        if not cls.instance:
            cls.users = {}
            cls.connections = {}
            cls.instance = ConnectionsService(chat_repository)
        return cls.instance

    #UPDATE TO HANDLE EMPTY GROUP CHATS TODO
    def has_connections_available(self):
        if len(self.connections) < self.MAX_CONNECTIONS:
            return {'response_type': 'auth', 'success': True}
        return {'response_type': 'auth', 'error': 'Server is full'}
    
    def add_connection(self, decoded_data, client_socket):
        self.users[decoded_data['user_id']] = {
            'username': decoded_data['username'], 
            'socket': client_socket
        }
        return {'response_type': 'auth', 'success': True}
    
    def preload_chat_conns(self):
        chats = self.chats_repository.get_chats_info()
        for chat in chats: 
            chat_conn = {
                'chat_name': chat['chat_name'],
                'subscribers': chat['subscribers'].split(',')
            }
    
            self.connections = {
                chat['chat_id']: chat_conn
            }

    def remove_user_connection(self, user_id):
        if user_id in self.users:
            del self.connections[user_id]

    def get_user_connection(self, conn_id, chat_id):
        found_user = self.chats_repository.get_chat_participant(conn_id, chat_id)
        if not found_user:
            return None
        if conn_id in self.users:
            return self.users[conn_id]
        return {
            'user_id': found_user['user_id'],
            'user_name': found_user['user_name']
        }
    
    def get_chat_connection(self, conn_id):
        # found_chat = self.chats_repository.get_chat_details(conn_id)
        # if found_chat == None:
        #     return None
        if conn_id in self.connections:
            return self.connections[conn_id]
        return None
     
    def get_available_users(self):
        available_users = []
        for conn_id, conn_data in self.users.items():
            available_users.append({
                'user_id': conn_id,
                'username': conn_data['username']
            })


        return {
                'success': True,
                'response_type': 'available_users', 
                'connections': available_users
            }
    
    def get_available_chats(self):
        available_connections = []

        for conn_id, conn_data in self.connections.items():
            if conn_data:
                available_connections.append({
                    'chat_id': conn_id,
                    'chat_name': conn_data['chat_name']
                })

        return {
                'success': True,
                'response_type': 'available_chats', 
                'connections': available_connections
            }

    def create_group_connection(self, decoded_data):
        user_id = decoded_data['user_id']
        chat_name = decoded_data['chat_name']
        if user_id not in self.users:
            return {
                'error': 'User not found',
                'response_type': 'create_group_connection'
            }
        chat_id = self.chats_repository.create_chat(user_id, chat_name)
        if chat_id not in self.connections:
            self.connections[chat_id] = {
                'chat_name': chat_name,
                'subscribers': {
                    user_id: self.users[user_id]
                }
            }
        return {
            'success': True,
            'response_type': 'create_group_connection'
        }

    def is_user_in_group_connection(self, decoded_data):
        pass

    def join_group_connection(self, decoded_data):
        user_id = decoded_data['user_id']
        chat_id = decoded_data['chat_id']

        if user_id not in self.users:
            return {
                'error': 'user not found',
                'response_type': 'join_group_connection'
            }
        
        if chat_id not in self.connections:
            return {
                'error': 'chat not found',
                'response_type': 'join_group_connection'
            }
        
        found_participation = self.chats_repository.get_chat_participant(user_id, chat_id)
        
        if not found_participation:
            self.chats_repository.add_chat_participant(chat_id, user_id)
        if user_id not in self.connections[chat_id]['subscribers']:
            self.connections[chat_id]['subscribers'].append(user_id)

        return { 'sucess': True, 'request_type': 'join_group_connection'}
        
    def left_group_connection(self, decoded_data):
        user_id = decoded_data['user_id']
        chat_id = decoded_data['chat_id']

        if user_id not in self.users:
            return {
                'error': 'User not found',
                'response_type': 'left_group_connection'
            }
        
        if chat_id not in self.connections:
            return {
                'error': 'User not found',
                'response_type': 'left_group_connection'
            }

        try:
            self.connections[chat_id].remove(user_id)
            return { 'sucess': True, 'request_type': 'left_group_connection' }
        except ValueError:
            return { 'error': 'user not subscribed to this chat', 'request_type': 'left_group_connection' }