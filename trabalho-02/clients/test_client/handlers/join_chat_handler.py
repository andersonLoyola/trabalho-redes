import os
import threading
from .base_handler import BaseHandler


class JoinChatHandler(BaseHandler):
    def __init__(self, conn, msg_service, file_storage_service):
        self.conn =  conn
        self.msg_service = msg_service
        self.file_storage_service = file_storage_service
        self.current_user_info = {}
        self.current_chat_info = {}
    
    # probably there is a bteer way but i'm tired of rthis shit
    def _format_group_message_to_send(self, message, attachment):
        if attachment:
             return {
                'sender_id': self.current_user_info['user_id'],
                'sender': self.current_user_info['username'],
                'chat_id': self.current_chat_info['chat_id'],
                'request_type': 'group_message',
                'attachment': attachment,
                'message': message,
            }
        
        return {
            'sender_id': self.current_user_info['user_id'],
            'chat_id': self.current_chat_info['chat_id'],
            'sender': self.current_user_info['username'],
            'request_type':  'group_message',
            'message': message,
            'attachment': ''
        }
    
    def _format_private_message_to_send(self, message, attachment):
        if attachment:
             return {
                'receiver_id': self.current_chat_info['chat_id'],
                'sender_id': self.current_user_info['user_id'],
                'sender': self.current_user_info['username'],
                'request_type': 'private_message',
                'attachment': attachment,
                'message': message,
            }
        
        return {
            'receiver_id': self.current_chat_info['chat_id'],
            'sender_id': self.current_user_info['user_id'],
            'sender': self.current_user_info['username'],
            'request_type':  'private_message',
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
            file_path = input('enter file path:')
            attachment = self.file_storage_service.load_file(file_path)
            return attachment

    def _on_join_group_chat_message(self):
        join_chat_goup_request = {
            'chat_id': self.current_chat_info['chat_id'],
            'user_id': self.current_user_info['user_id'],
            'request_type': 'join_group_connection'
        }
        self.msg_service.send_message(self.conn, join_chat_goup_request)
        response = self.msg_service.receive_message(self.conn)
        if not response:
            pass
        elif 'success' in response and response['response_type']:
            message = self._format_group_message_to_send(
                f'{self.current_user_info['username']} has joined the chat', 
                ''
            )
            self.msg_service.send_message(self.conn, message)
        elif 'error' in response:
            self.handle_error(response['error'], 'JOINING GROUP CHAT CONNECTION')
    
    def _left_group_chat(self):
        message = {
            'chat_id': self.current_chat_info['chat_id'],
            'user_id': self.current_chat_info['user_id'],
            'request_type': 'left_group_connection',
        }

    def _on_received_messages(self):
        while True:
            response = self.msg_service.receive_message(self.conn)
            if response == None:
                pass
            elif response['response_type'] == 'group_message' and response:
                if 'chat_id' in response and self.current_chat_info['chat_id'] == response['chat_id']:
                    formatted_message = self._format_received_message(response)
                    print(formatted_message)
            elif response['response_type'] == 'private_message' and response:
                if 'receiver_id' in response and self.current_chat_info['chat_id'] == response['chat_id']:
                    formatted_message = self._format_received_message(response)
                    print(formatted_message)
            elif response['response_type'] == 'left_group_connection':
                break
        return

    def _handle_disconnect_from_chat():
        pass

    def handle_join_group_chat(self, chat_info, current_user_info):
        self.current_user_info = current_user_info
        self.current_chat_info = chat_info
        self._on_join_group_chat_message()# idk if that's really needed but feels nice to have
        receive_messages_thread = threading.Thread(target=self._on_received_messages, daemon=True)
        receive_messages_thread.start()
        while True:
            attachment = ''
            message = str(input("> "))
            if message == '\\q':
                break
            elif message == '\\fu':
                attachment = self._on_file_upload_request()
            message = self._format_group_message_to_send(message, attachment)
            self.msg_service.send_message(self.conn, message)
        
    def handle_join_private_chat(self, current_user_info, chat_info):
        self.current_user_info = current_user_info
        self.current_chat_info = chat_info
        receive_messages_thread = threading.Thread(target=self._on_received_messages, daemon=True)
        receive_messages_thread.start()
        while True:
            attachment = ''
            message = str(input("> "))
            if message == '\\q':
                break
            elif message == '\\fu':
                attachment = self._on_file_upload_request()
            message = self._format_private_message_to_send(message, attachment)
            self.msg_service.send_message(self.conn, message) 