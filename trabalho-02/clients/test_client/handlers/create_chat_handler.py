import os
from .base_handler import BaseHandler

class CreateChatHandler(BaseHandler):
    chat_api = {}

    def __init__(self, chat_api):
       self.chat_api = chat_api

    def _create_chat_input(self, token):
        os.system('cls')
        chat_name = input('chat name: ')
        response = self.chat_api.create_chat(token, chat_name)
        return response
      

    """
        TODO: same thing here, include a option to left earlier
    """  
    def handle_chat_creation(self, token):
        while True:
            response = self._create_chat_input(token)
            if ('error' in response):
                input(response['error'])
            else:
                return response