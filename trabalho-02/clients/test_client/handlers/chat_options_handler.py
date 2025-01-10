import os
import sys
from .base_handler import BaseHandler

class ChatOptionHandler(BaseHandler):
    
    def __init__(self, chatuba_api):
        self.chatuba_api = chatuba_api   

    def _print_connected_users_options(self, response):
        os.system('cls')
        print('0. go back')
        for index in range(len(response['connections'])):
            print(f'{index +1 }. {response['connections'][index]['username']}')

        choose = int(input('choose chat: '))
        if (choose == 0): 
            return
        elif choose > len(response):
            print('invalid choise') # this is not gonna  work, deal with this once the project is dosne maybe TODO:
        else:
            return response['connections'][choose-1]
   
    def handle_group_chats_options(self, token):
        while True:
            os.system('cls')
            print('0. go back')
            response = self.chatuba_api.list_available_group_chats(token)
            if 'error' in response:
                input(response['error'])
                sys.exit()
            for index in range(len(response['chats'])):
                print(f'{index + 1 }. {response['chats'][index]['chat_name']}')
            choose = int(input('choose chat: '))
            if (choose == 0): 
                return
            elif choose > len(response['chats']):
                input('invalid choice') # this is not gonna  work, deal with this once the project is dosne maybe TODO:
            else:
                return response['chats'][choose-1]
        
    def handle_available_users_chats(self, user_info):
        pass