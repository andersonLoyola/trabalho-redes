import traceback
import threading

class ConnectionsService: 
    users = {}
    group_chats = {}
    instance = None
    
    def __init__(self, rest_service):
        self.MAX_CONNECTIONS = 50
        self.rest_service = rest_service
        self.lock = threading.Lock()

    @classmethod
    def get_instance(cls, rest_service):
        if not cls.instance:
            cls.users = {}
            cls.group_chats = {}
            cls.instance = ConnectionsService(rest_service)
        return cls.instance
   
    def has_connections_available(self):
        sessions_count = 0
        for user in self.users:
            sessions_count += len(user['sessions'].keys())
        if sessions_count < self.MAX_CONNECTIONS:
            return { 'action': 'connection', 'success': True }
        return { 'action': 'connection', 'error': 'Server is full' }
    
    def connect_user(self, decoded_data):
        user_id = decoded_data['user_id']

        if user_id not in self.users:
            self.users[user_id] = {
                'sessions': {}
            }
            return {'action': 'connection', 'success': True}

        if (len(self.users[user_id]['sessions'].keys()) > 3):
            return {
                'action': 'connection', 
                'error': 'max user simultaneous connection reached'
            }
        
        return {'action': 'connection', 'success': True}
            
    def add_user_chat_session(self, user_id, chat_id, client_socket):
        try:
            with self.lock:
                if user_id not in self.users:
                    return {
                        'action': 'join_chat',
                        'error': 'user not found'
                    }
                if (len(self.users[user_id]['sessions'].keys()) > 3):
                    return {
                        'action': 'join_chat', 
                        'error': 'max user simultaneous connection reached'
                    }
                if (chat_id in self.users[user_id]['sessions']):
                    return {
                        'action': 'join_chat', 
                        'error': 'already connected to this chat'
                    }
                if (chat_id in self.group_chats):
                    self.group_chats[chat_id]['subscribers'].append(user_id)
                self.users[user_id]['sessions'][chat_id] = client_socket
                
                return {
                    'success': True
                }
        
        except Exception as e:
            print(e)
            traceback.print_exc()

    def load_group_chats(self):
        try:
            with self.lock:
                response = self.rest_service.get_group_chats()
                for chat in response['chats']: 
                    chat_id = chat['chat_id']
                    chat_conn = {
                        'chat_name': chat['chat_name'],
                        'subscribers': chat['subscribers'].split(',')
                    }
                    self.group_chats[chat_id] = chat_conn          
        except Exception as e:
            traceback.print_exc()
            print(e)

    def remove_user_chat_session(self, user_id, chat_id):
        if user_id in self.users and chat_id in self.users[user_id]['sessions'][chat_id]:
            del self.users[user_id]['sessions'][chat_id]
        
    def get_user_connection(self, user_id, chat_id):
        try: 
            if user_id not in self.users:
                return {
                    # 'action': 'join_chat',
                    'error': f'user {user_id} not found'
                }
            
            if chat_id not in self.users[user_id]['sessions']:
                return {
                    'error': f'user {user_id} not member of {chat_id} at this momeent'
                }
            
            return {
                'success': True,
                'user_id': user_id,
                'conn': self.users[user_id]['sessions'][chat_id]
            }

        except Exception as e:
            traceback.print_exc()
            print(e)
    
    def get_chat_connection(self, conn_id):
        try:
            if conn_id in self.group_chats:
                return self.group_chats[conn_id]
            return None
        except Exception as e:
            traceback.print_exc()
            print(e)
     
    def get_available_users(self):
        available_users = []
        for conn_id, conn_data in self.users.items():
            available_users.append({
                'user_id': conn_id,
                'username': conn_data['username']
            })

        return {
                'success': True,
                'action': 'available_users', 
                'connections': available_users
            }
    
    def get_available_chats(self):
        try:
            with self.lock:
                available_connections = []
                for conn_id, conn_data in self.group_chats.items():
                    if conn_data:
                        available_connections.append({
                            'chat_id': conn_id,
                            'chat_name': conn_data['chat_name']
                        })

                return {
                        'success': True,
                        'action': 'available_chats', 
                        'connections': available_connections
                    }
        except Exception as e:
            traceback.print_exc()
            print(e)

    def remove_user_active_session(self, user_id, client_socket):
        if user_id not in self.users:
            return
        user_sessions = self.users[user_id]['sessions']
        for session_id, socket in user_sessions.items():
            if socket == client_socket:
                del user_sessions[session_id]
                return
        
    def left_group_connection(self, decoded_data):
        try:
            with self.lock:
                user_id = decoded_data['user_id']
                chat_id = decoded_data['chat_id']

                if user_id not in self.users:
                    return {
                        'error': 'User not found',
                        'action': 'left_group_connection'
                    }
                if chat_id not in self.group_chats:
                    return {
                        'error': 'Chat not found',
                        'action': 'left_group_connection'
                    }
                self.group_chats[chat_id].remove(user_id)
                return { 'sucess': True, 'action': 'left_group_connection' }
        except ValueError:
            return { 'error': 'user not subscribed to this chat', 'action': 'left_group_connection' }
        except Exception as e:
            traceback.print_exc()
            print(e)