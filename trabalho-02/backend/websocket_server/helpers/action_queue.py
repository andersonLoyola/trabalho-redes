from queue import Queue
import traceback

class ActionsQueue:
    instance = None
    actions = {}

    def __init__(self, chatuba_rest_service):
        self.chatuba_rest_service = chatuba_rest_service
        self.actions = Queue(0)

    @classmethod
    def get_instance(cls, chatuba_rest_service):
        if (cls.instance == None):
            cls.instance = cls(chatuba_rest_service)
        return cls.instance

    def add_action(self, action):
        self.actions.put(action)

    def store_group_message_action(self, message):
        try:
            response = self.chatuba_rest_service.store_group_message_request(message)
            return response
        except Exception as e:
            traceback.print_exc()
            print(e)
  
    def store_private_message_action(self, message):
        try:
            response = self.chatuba_rest_service.store_private_message_request(message)
            return response
        except Exception as e:
            traceback.print_exc()
            print(e)
  
    def join_group_chat_action(self, message):
        try:
            chat_id = message['chat_id']
            user_id = message['user_id']
            response = self.chatuba_rest_service.join_group_chat_request(chat_id, user_id)
            return response
        except Exception as e:
            traceback.print_exc()
            print(e)
    
    def run(self):
        while(True):
            action = self.actions.get()
            if action is None:
                pass
            elif action['action'] == 'group_message':
                self.store_group_message_action(action)
            elif action['action'] == 'private_message':
                self.store_private_message_action(action)
            elif action['action'] == 'join_group_chat':
                self.store_private_message_action(action)