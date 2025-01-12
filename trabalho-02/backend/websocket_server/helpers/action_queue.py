import traceback
from queue import Queue

class ActionsQueue:
    instance = None
    actions = {}

    def __init__(self, rest_service):
        self.rest_service = rest_service
        self.actions = Queue(0)

   
    def add_action(self, action):
        self.actions.put(action)

    def store_group_message_action(self, message):
        try:
            response = self.rest_service.store_group_message_request(
                message['sender_id'],
                message['chat_id'],
                message['receivers'],
                message['message'],
                message['attachment']
            )
            return response
        except Exception as e:
            traceback.print_exc()
            print(e)
  
    def store_private_message_action(self, message):
        try:
            response = self.rest_service.store_private_message_request(message['sender_id'], message['receiver_id'], message['message'], message['attachment'])
            return response
        except Exception as e:
            traceback.print_exc()
            print(e)
  
    def join_group_chat_action(self, message):
        try:
            chat_id = message['chat_id']
            session_id = message['session_id']
            response = self.rest_service.join_group_chat_request(chat_id, session_id)
            return response
        except Exception as e:
            traceback.print_exc()
            print(e)
    
    def left_group_chat_action(self, message):
        try:
            session_id = message['session_id']
            chat_id = message['chat_id']
            response = self.rest_service.left_group_chat_request(chat_id, session_id)
            return response
        except Exception as e:
            traceback.print_exc()
            print(e)
    
    def create_group_chat_action(self, message):
        try:
            response = self.rest_service.create_group_chat_request(
                message['session_id'],
                message['chat_id'],
                message['chat_name']
            )
            return response
        except Exception as e:
            traceback.print_exc()
            print(e)

    def disconnect_user_action(self, message):
        try:
            response = self.rest_service.disconnect_user_request(
                message['user_id'],
                message['session_id'],
            )
            return response
        except Exception as e:
            traceback.print_exc()
            print(e)
            

    def run(self):
        while(True):
            action = self.actions.get()
            if action is None:
                pass
            try:
                if action['action'] == 'group_message':
                    response = self.store_group_message_action(action)
                    print(f'{action['action']}: {response}')
                elif action['action'] == 'private_message':
                    response = self.store_private_message_action(action)
                    print(f'{action['action']}: {response}')
                elif action['action'] == 'join_group_chat':
                    response = self.join_group_chat_action(action)
                    print(f'{action['action']}: {response}')
                elif action['action'] == 'store_group_chat':
                    response = self.create_group_chat_action(action)
                    print(f'{action['action']}: {response}')
                elif action['action'] == 'left_group_chat':
                    response = self.left_group_chat_action(action)
                    print(f'{action['action']}: {response}')
                elif action['action'] == 'disconnect_user':
                    response = self.disconnect_user_action(action)
                    print(f'{action['action']}: {response}')
            except Exception as e:
                traceback.print_exc()
                print(e)
            finally:
                self.actions.task_done()