import os
import sys
import threading
from .base_handler import BaseHandler

class PrivateChatHandler(BaseHandler):
    msg_service = {}
    current_user_info = {}
    file_storage_service = {}

    def __init__(self, msg_service, file_storage_service):
        self.msg_service = msg_service
        self.file_storage_service = file_storage_service
                             
    def _format_private_message_to_send(self, message, attachment):
        if attachment:
             return {
                'receiver_id': self.current_chat_info['receiver_id'],
                'receiver_session': self.current_chat_info['receiver_session'],
                'sender': self.current_user_info['username'],
                'sender_id': self.current_user_info['session_id'],
                'action': 'private_message',
                'attachment': attachment,
                'message': message,
            }
        
        return {
            'receiver_id': self.current_chat_info['receiver_id'],
            'receiver_session': self.current_chat_info['receiver_session'],
            'sender': self.current_user_info['username'],
            'sender_id': self.current_user_info['session_id'],
            'action': 'private_message',
            'message': message,
            'attachment': '',
        }
    
    def _format_received_message(self, message):
        if not message['attachment']:
            return  f'{message['sender']}> {message['message']}'
        return  f'{message['sender']}> {message['attachment']['file_name']}'

    def _on_file_upload_request(self):
            os.system('cls')
            file_path = input('enter file path: ')
            attachment = self.file_storage_service.load_file(file_path)
            return attachment
    
    def _left_private_chat(self):
        left_private_chat_message = {
            'receiver_id': self.current_chat_info['receiver_id'],
            'user_id': self.current_user_info['session_id'],
            'action': 'left_private_connection',
        }
        self.msg_service.send_message(self.conn, left_private_chat_message)

    def _on_received_messages(self):
        while True:
            response = self.msg_service.receive_message(self.conn)
            if response == None:
                pass
            elif response['action'] == 'private_message':
                if 'attachment' in response and response['attachment'] != '':
                    self.file_storage_service.save_file(self.current_user_info['session_id'], response['attachment'])
                formatted_message = self._format_received_message(response)
                print(formatted_message)
            elif response['action'] == 'left_private_connection':
                break

    def _connect(self):
        join_chat_request = {
            'receiver_id': self.current_chat_info['receiver_id'],
            'receiver_session': self.current_chat_info['receiver_session'],
            'session_id': self.current_user_info['session_id'],
            'user_id': self.current_user_info['id'],
            'action': 'join_private_chat'
        }
        self.msg_service.send_message(self.conn, join_chat_request)
        response = self.msg_service.receive_message(self.conn)
        return response  
    

    def handle_show_private_chats(self, conn, current_user_info):
        self.conn = conn
        self.current_user_info = current_user_info
        while True:
            os.system('cls')
            show_private_chats_action = {
                'session_id': self.current_user_info['session_id'],
                'user_id': self.current_user_info['id'],
                'action': 'show_private_chats'
            }
            self.msg_service.send_message(self.conn, show_private_chats_action)
            response = self.msg_service.receive_message(self.conn)
            if 'error' in response:
                input(response['error'])
            elif response['action'] == 'show_private_chats':
                print('0. go back;')
                private_chats = response['chats']
                for index in range(len(private_chats)):
                    print(f'{index + 1}. {private_chats[index]['user_name']}')
                choice = int(input('chat option: '))
                if choice == 0:
                    return
                elif choice - 1 <= len(private_chats):
                    choosen_chat = private_chats[choice - 1]
                    self.current_chat_info = {
                        'receiver_id': choosen_chat['user_id'],
                        'receiver_session': choosen_chat['session_id']
                    }
                    self.handle_join_private_chat()
                else:
                    input('invalid option')
        
    
    def handle_join_private_chat(self):
        self._connect() # TODO: ADD ERROR HANDLING LATER 
        receive_messages_thread = threading.Thread(target=self._on_received_messages, daemon=True)
        receive_messages_thread.start()
        os.system('cls')
        while True:
            attachment = ''
            message = str(input())
            if message == '\\q':
                message = ''
                self._left_private_chat()
                break
            elif message == '\\fu':
                attachment = self._on_file_upload_request()
                message = ''
            if len(message.strip()) > 0 or attachment != '':     
                message = self._format_private_message_to_send(message, attachment)
                self.msg_service.send_message(self.conn, message)
                sys.stdout.write("\033[F\033[K") # JUST CLEARS THE INPUT LINE
    