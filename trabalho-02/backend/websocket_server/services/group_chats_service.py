import uuid
import json
import threading

class GroupChatsService:

    group_chats = {}
    rest_service = {}
    actions_service = {}

    def __init__(self, actions_service, rest_service):
        self.lock = threading.Lock()
        self.rest_service = rest_service
        self.actions_service = actions_service
       
    def load_group_chats_from_service(self):
        response = self.rest_service.get_group_chats()  
        if not 'chats' in response:
            print(f'load_group_chats_from_service: cannot load chats from database')
            return
        for chat in response['chats']:
            if chat['subscribers'] == None:
                self.group_chats[chat['chat_id']] = {
                'chat_name': chat['chat_name'],
                'subscribers': []
                }
            else:
                self.group_chats[chat['chat_id']] = {
                    'chat_name': chat['chat_name'],
                    'subscribers': json.loads(chat['subscribers'])
                }

    def create_group_chat(self, user_id, session_id, chat_name):
        for group_chat in self.group_chats.values():
            if group_chat['chat_name'] == chat_name:
                return { 'error': 'chat already exists' }
        
        chat_id = str(uuid.uuid4())
        store_group_chat_action = {
            'user_id': user_id,
            'chat_id': chat_id,
            'chat_name': chat_name,
            'session_id': session_id,
            # 'callback': self.load_group_chats_from_service,
            'action': 'store_group_chat'
        }

        self.group_chats[chat_id] = {
            'chat_name': chat_name,
            'subscribers': [
                {
                    'user_id': user_id,
                    'session_id': session_id,
                }
            ]
        }
        self.actions_service.add_action(store_group_chat_action)
        return { 'success': True, 'action': 'create_group_chat' }     

    def add_user_chat_session(self, user_id, session_id, chat_id):
        with self.lock:
            if (chat_id not in self.group_chats):
                return {
                    'error': 'chat not found',
                    'action': 'join_chat'
                }
            self.group_chats[chat_id]['subscribers'].append({
                'user_id': user_id,
                'session_id': session_id
            })
            self.actions_service.add_action({
                'session_id': session_id,
                'chat_id': chat_id,
                'action': 'join_group_chat'
            })
            return {
                'success': True,
                'action': 'join_chat'
            }
    
        

    def remove_user_chat_session(self, user_id, session_id, chat_id):
        if chat_id not in self.group_chats:
            return {
                'error': f'chat: {chat_id} not found'
            }
        for user_session in self.group_chats[chat_id]['subscribers']:
            if user_session['session_id'] == session_id and user_session['user_id'] == user_id:
                del user_session
                return 
    
    
    def get_chat_connection(self, conn_id):
        try:
            if conn_id in self.group_chats:
                return self.group_chats[conn_id]
            return None
        except Exception as e:
            print(f'{conn_id} get_chat_connection: {str(e)}')    
    
    def show_group_chats(self):
        with self.lock:
            available_group_chats = []
            for conn_id, conn_data in self.group_chats.items():
                if conn_data:
                    available_group_chats.append({
                        'chat_id': conn_id,
                        'chat_name': conn_data['chat_name']
                    })
            return {
                    'success': True,
                    'action': 'show_group_chats', 
                    'chats': available_group_chats
                }
     
    
    def left_group_connection(self, decoded_data):
        with self.lock:
            user_id = decoded_data['user_id']
            session_id = decoded_data['session_id']
            chat_id = decoded_data['chat_id']
            
            if chat_id not in self.group_chats:
                return {
                    'error': 'Chat not found',
                    'action': 'left_group_connection'
                }
            for subscriber in self.group_chats[chat_id]['subscribers']:
                if subscriber['user_id'] == user_id and subscriber['session_id'] == session_id:
                    del subscriber
                    self.actions_service.add_action({
                        'user_id': user_id,
                        'chat_id': chat_id,
                        'session_id': session_id,
                        'action': 'left_group_chat'
                    })
            return { 'sucess': True, 'action': 'left_group_connection' }