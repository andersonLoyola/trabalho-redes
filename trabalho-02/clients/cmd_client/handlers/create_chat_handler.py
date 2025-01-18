import os
from .base_handler import BaseHandler

class CreateChatHandler(BaseHandler):
    conn = {}
    messages_service = {}

    def __init__(self, messages_service):
       self.messages_service = messages_service

    def _create_chat_input(self, current_chat_info):
        os.system('cls')
        chat_name = input('chat name: ')
        create_group_chat_message = {
            'chat_name': chat_name,
            'action': 'create_group_chat',
            'user_id': current_chat_info['id'],
            'session_id': current_chat_info['session_id']
        } 
        self.messages_service.send_message(self.conn, create_group_chat_message)
        
    """
        TODO: same thing here, include a option to left earlier
    """  
    def handle_chat_creation(self, conn, current_chat_info):
        self.conn = conn
        while True:
            self._create_chat_input(current_chat_info)
            response = self.messages_service.receive_message(self.conn)
            if not response:
                continue
            elif 'error' in response:
                input(response['error'])
            else: 
                return response