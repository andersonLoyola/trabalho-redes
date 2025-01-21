import os
from .base_handler import BaseHandler

class CreateChatHandler(BaseHandler):
    conn = {}
    messages_service = {}

    def __init__(self, messages_service):
       self.messages_service = messages_service

    def handle_chat_creation(self, conn, current_chat_info):
        self.conn = conn
        while True:
            os.system('cls')
            print('type \q to quit')
            response = str(input('chat name: '))
            if response == '\\q':
                return
            create_group_chat_message = {
                'chat_name': response,
                'action': 'create_group_chat',
                'user_id': current_chat_info['id'],
                'session_id': current_chat_info['session_id']
            } 
            self.messages_service.send_message(self.conn, create_group_chat_message)
            response = self.messages_service.receive_message(self.conn)
            if not response:
                continue
            elif 'error' in response:
                input(response['error'])
            else: 
                return response