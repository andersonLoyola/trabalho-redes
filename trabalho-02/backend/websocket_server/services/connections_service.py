import threading

class ConnectionsService: 
    users = {}
    group_chats = {}
    instance = None
    
    def __init__(self, rest_service):
        self.MAX_CONNECTIONS = 50
        self.lock = threading.Lock()
        self.rest_service = rest_service

    # TODO: remove this shit later
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
    
    def connect_user(self, decoded_data, client_socket):
        user_id = decoded_data['user_id']
        session_id = decoded_data['session_id']

        if user_id not in self.users:
            self.users[user_id] = {
                'user_name': decoded_data['user_name'],
                'sessions': {
                    session_id: {
                        'status': 'active',
                        'conn': client_socket,
                        'chat_id': ''
                    }
                }
            }
            return {'action': 'connection', 'success': True}

        if (len(self.users[user_id]['sessions'].keys()) > 3):
            return {
                'action': 'connection', 
                'error': 'max user simultaneous connection reached'
            }
        
        self.users[user_id]['sessions'][session_id] = {
            'status': 'active',
            'conn': client_socket
        }
        
        return {'action': 'connection', 'success': True}

    def get_user_session(self, user_id, session_id, chat_id):
        if user_id not in self.users:
            return {
                'error': f'user {user_id} not found'
            }
        elif session_id not in self.users[user_id]['sessions']:
            return {
                'error': f'user {user_id} not found'
            }
        user_session = self.users[user_id]['sessions'][session_id]
        if user_session['status'] != 'active' and user_session['chat_id'] != chat_id:
            return {
                'error': f'session {session_id} from user: {user_id} is not available'
            }
        return {
            'success': True,
            'user_id': user_id,
            'conn': self.users[user_id]['sessions'][session_id]['conn']
        }
    
    def update_session_status(self, user_id, session_id, status, chat_id):
        if user_id not in self.users:
            return {
                'error': 'user_not found'
            }
        elif session_id not in self.users[user_id]['sessions']:
            return {
                'error': 'session not found'
            }
        self.users[user_id]['sessions'][session_id]['status'] = status
        self.users[user_id]['sessions'][session_id]['chat_id'] = chat_id

    def show_private_chats(self, decoded_data):
        show_private_chats = []
        current_session_id = decoded_data['session_id']
        for conn_id, conn_data in self.users.items():
            for session_id, session_data in conn_data['sessions'].items():
                current_chat = session_data['chat_id']
                if current_chat == current_session_id or (current_chat == '' and session_id != current_session_id) :
                    show_private_chats.append({
                            'user_id': conn_id,
                            'session_id': session_id,
                            'user_name': conn_data['user_name']
                        })
        return {
                'success': True,
                'action': 'show_private_chats', 
                'chats': show_private_chats
            }
    
    def find_user_active_session(self, user_id, client_socket):
        if user_id not in self.users:
            return None
        user_sessions = self.users[user_id]['sessions']
        for session_id, session_data in user_sessions.items():
            if session_data['conn'] == client_socket:
                return {
                    'user_id': user_id,
                    'session_id': session_id,
                }
        return None
    
    def remove_user_active_session(self, user_id, session_id):
        if user_id not in self.users:
            return 
        elif session_id not in self.users[user_id]['sessions']:
            return
        del self.users[user_id]['sessions'][session_id]