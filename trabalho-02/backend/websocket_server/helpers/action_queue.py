import json
from queue import Queue

class ActionsQueue:
    instance = None
    actions = {}
    crypto_serializer = {}

    def __init__(self, rest_service, crypto_serializer):
        self.crypto_serializer = crypto_serializer
        self.rest_service = rest_service
        self.actions = Queue(0)

    def add_action(self, action):
        self.actions.put(action)

    def _log_error(self, action, error):
        if 'session_id' in action:
            return f'[{action['session_id']}][{action['action']}]: {str(error)}'
        
        return f'[{action['sender_id']}][{action['action']}]: {str(error)}'
            
    def store_group_message_action(self, message):
        message_bytes = json.dumps({
            'sender_id': message['sender_id'],
            'chat_id': message['chat_id'],
            'receivers': message['receivers'],
            'message': message['message'],
            'attachment': message['attachment']
        }).encode('utf-8')
        encrypted_message = self.crypto_serializer.encrypt(message_bytes)
        response = self.rest_service.store_group_message_request(encrypted_message)
        return response

    def store_private_message_action(self, message):
        message_bytes = json.dumps({
            'sender_id': message['sender_id'],
            'receiver_id': message['receiver_id'],
            'message': message['message'],
            'attachment': message['attachment']
        }).encode('utf-8')
        encrypted_message = self.crypto_serializer.encrypt(message_bytes)
        response = self.rest_service.store_private_message_request(encrypted_message)
        return response
       
    def join_group_chat_action(self, message):
        chat_id = message['chat_id']
        session_id = message['session_id']
        response = self.rest_service.join_group_chat_request(chat_id, session_id)
        return response
    
    def left_group_chat_action(self, message):
        session_id = message['session_id']
        chat_id = message['chat_id']
        response = self.rest_service.left_group_chat_request(chat_id, session_id)
        return response
           
    def create_group_chat_action(self, message):
        message_bytes = json.dumps({
            'session_id':  message['session_id'],
            'chat_id':  message['chat_id'],
            'chat_name':  message['chat_name'],
        }).encode('utf-8')
        encrypted_message = self.crypto_serializer.encrypt(message_bytes)
        response = self.rest_service.create_group_chat_request(encrypted_message)
        return response
      
    def disconnect_user_action(self, message):
        message_bytes = json.dumps({
            'user_id': message['user_id'],
            'session_id': message['session_id'],
        }).encode('utf-8')
        encrypted_message = self.crypto_serializer.encrypt(message_bytes)
        response = self.rest_service.disconnect_user_request(encrypted_message)
        return response
      
    def run(self):
        while True:
            try:
                action = self.actions.get()
                if action is None:
                    pass
                if action['action'] == 'group_message':
                    response = self.store_group_message_action(action)
                    print(f'[{action['sender_id']}][{action['action']}][{action['chat_id']}]: {response}')
                elif action['action'] == 'private_message':
                    response = self.store_private_message_action(action)
                    print(f'[{action['sender_id']}][{action['action']}][{action['receiver_id']}]: {response}')
                elif action['action'] == 'join_group_chat':
                    response = self.join_group_chat_action(action)
                    print(f'[{action['session_id']}][{action['action']}][{action['chat_id']}]: {response}')
                elif action['action'] == 'store_group_chat':
                    response = self.create_group_chat_action(action)
                    print(f'[{action['session_id']}][{action['action']}][{action['chat_id']}]: {response}')
                elif action['action'] == 'left_group_chat':
                    response = self.left_group_chat_action(action)
                    print(f'[{action['session_id']}][{action['action']}][{action['chat_id']}]: {response}')
                elif action['action'] == 'disconnect_user':
                    response = self.disconnect_user_action(action)
                    print(f'[{action['user_id']}][{action['action']}][{action['session_id']}]: {response}')
            except Exception as e:
                print(self._log_error(action, e))
            finally:
                self.actions.task_done()