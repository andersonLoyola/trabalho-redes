import os

class CreateChatHandler:
    def __init__(self, msg_service, conn):
        self.msg_service = msg_service
        self.current_user = {}
        self.current_chat = {}
        self.conn = conn

    def _create_chat_input(self, user_info):
        os.system('cls')
        chat_name = input('chat name: ')
        message = {
            'chat_name': chat_name,
            'user_id': user_info['user_id'],
            'request_type': 'create_group_connection'
        }
        self.msg_service.send_message(self.conn, message)
      
        

    def handle_chat_creation(self, user_info):
        while True:
            self._create_chat_input(user_info)
            response = self.msg_service.receive_message(self.conn)
            if not response:
                pass
            if 'success' in response and response['response_type'] == 'create_group_connection':
                return
            