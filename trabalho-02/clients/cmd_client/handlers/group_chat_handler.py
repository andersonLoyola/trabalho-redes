import os
import sys
import threading
from .base_handler import BaseHandler


class GroupChatHandler(BaseHandler):
    
    conn = {}
    msg_service = {}
    current_user_info = {}
    file_storage_service = {}

    def __init__(self, msg_service, file_storage_service):
        self.msg_service = msg_service
        self.file_storage_service = file_storage_service
        
    def _show_group_chat_options(self):
        os.system('cls')
        while True:
            show_group_chats_action = {
                'user_id': self.current_user_info['id'],
                'session_id': self.current_user_info['session_id'],
                'action': 'show_group_chats'
            }
            self.msg_service.send_message(self.conn,  show_group_chats_action)
            response = self.msg_service.receive_message(self.conn)
            if not response:
                pass
            elif 'error' in response:
                input(response['error'])
            elif response['action'] == 'show_group_chats':
                group_chats = response['chats']
                for index in range(len(group_chats)):
                    print(f'{index + 1}. {group_chats[index]['chat_name']}')
                choice = int(input('chat option: '))
                if choice == 0:
                    break
                elif choice - 1 <= len(group_chats):
                    return group_chats[choice-1]
                else:
                    input('invalid option')
                        
    def _format_group_message_to_send(self, message, attachment):
        if attachment:
            return {
                'sender_id': self.current_user_info['session_id'],
                'sender': self.current_user_info['username'],
                'chat_id': self.current_chat_info['chat_id'],
                'action': 'group_message',
                'attachment': attachment,
                'message': message,
            }
        return {
            'sender_id': self.current_user_info['session_id'],
            'chat_id': self.current_chat_info['chat_id'],
            'sender': self.current_user_info['username'],
            'action':  'group_message',
            'message': message,
            'attachment': ''
        }
    
    def _format_received_message(self, message):
        template = f'{message['sender']}> {message['message']}'
        if not message['attachment']:
            return template
        return f'{template}\nattachment:{message['attachment']}'

    def _on_file_upload_request(self):
            os.system('cls')
            file_path = input('enter file path: ')
            attachment = self.file_storage_service.load_file(file_path)
            return attachment
    
    def _left_group_chat(self):
        left_group_chat_message = {
            'action': 'left_group_chat',
            'chat_id': self.current_chat_info['chat_id'],
            'user_id': self.current_user_info['id'],
            'session_id': self.current_user_info['session_id'],
        }
        self.msg_service.send_message(self.conn, left_group_chat_message)

    def _on_received_messages(self):
        while True:
            response = self.msg_service.receive_message(self.conn)
            if response == None:
                pass
            elif response['action'] == 'group_message':
                if 'attachment' in response and response['attachment'] != '':
                    self.file_storage_service.save_file(self.current_user_info['id'], response['attachment'])
                formatted_message = self._format_received_message(response)
                print(formatted_message)
            elif response['action'] == 'left_group_connection':
                input(response)
                break
        
    def _connect(self):
        try:
            join_chat_request = {
                'user_id': self.current_user_info['id'],
                'session_id': self.current_user_info['session_id'],
                'chat_id': self.current_chat_info['chat_id'],
                'action': 'join_group_chat'
            }
            self.msg_service.send_message(self.conn, join_chat_request)
            response = self.msg_service.receive_message(self.conn)
            return response  
        except Exception as e:
            input(e)

    def handle_show_group_chats(self, conn, current_user_info):
        try:
            self.conn = conn
            self.current_user_info = current_user_info
            while True:
                choosen_chat = self._show_group_chat_options()
                self.current_chat_info = choosen_chat
                self.handle_join_group_chat()
        except Exception as e:
            print(e)
        
    def handle_join_group_chat(self):
        try:
            response = self._connect() # TODO: ADD ERROR HANDLING LATER 
            receive_messages_thread = threading.Thread(target=self._on_received_messages, daemon=True)
            receive_messages_thread.start()
            os.system('cls')
            while True:
                attachment = ''
                message = str(input())
                if message == '\\q':
                    message = ''
                    input(self._left_group_chat())
                    break
                elif message == '\\fu':
                    attachment = self._on_file_upload_request()
                    message = ''
                if len(message.strip()) > 0 or attachment != '':     
                    message = self._format_group_message_to_send(message, attachment)
                    self.msg_service.send_message(self.conn, message)
                    sys.stdout.write("\033[F\033[K") # JUST CLEARS THE INPUT LINE
        except Exception as e:
            self.handle_error(e)