import os
import threading
from .base_handler import BaseHandler


class GroupChatHandler(BaseHandler):
    msg_service = {}
    token_service = {}
    current_user_info = {}
    file_storage_service = {}

    def __init__(self, token_service, msg_service, file_storage_service):
        self.msg_service = msg_service
        self.token_service = token_service
        self.file_storage_service = file_storage_service
        
    
    def _format_group_message_to_send(self, message, attachment):
        if attachment:
             return {
                'sender_id': self.current_user_info['id'],
                'sender': self.current_user_info['username'],
                'chat_id': self.current_chat_info['chat_id'],
                'action': 'group_message',
                'attachment': attachment,
                'message': message,
            }
        
        return {
            'sender_id': self.current_user_info['id'],
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
            file_path = input('enter file path:')
            attachment = self.file_storage_service.load_file(file_path)
            return attachment
    
    def _left_group_chat(self):
        left_group_chat_message = {
            'chat_id': self.current_chat_info['chat_id'],
            'user_id': self.current_chat_info['user_id'],
            'action': 'left_group_connection',
        }
        self.msg_service(self.conn, left_group_chat_message)

    def _on_received_messages(self, conn):
        while True:
            response = self.msg_service.receive_message(conn)
            if response == None:
                pass
            elif response['action'] == 'group_message':
                if 'chat_id' in response and self.current_chat_info['chat_id'] == response['chat_id']:
                    formatted_message = self._format_received_message(response)
                    print(formatted_message)
            elif response['action'] == 'left_group_connection':
                break
        return

    def _connect(self, conn):
        try:
            join_chat_request = {
                'chat_id': self.current_chat_info['chat_id'],
                'user_id': self.current_user_info['id'],
                'action': 'join_chat'
            }
            self.msg_service.send_message(conn, join_chat_request)
            response = self.msg_service.receive_message(conn)
            return response  
        except Exception as e:
            input(e)
            
    def handle_join_group_chat(self, conn, chat_info, token):
        self.current_chat_info = chat_info
        self.current_user_info = self.token_service.decode_token(token)

        response = self._connect(conn)
        receive_messages_thread = threading.Thread(target=self._on_received_messages, args=(conn,) , daemon=True)
        receive_messages_thread.start()
        while True:
            attachment = ''
            message = str(input(" "))
            if message == '\\q':
                message = ''
                self._left_group_chat()
                break
            elif message == '\\fu':
                attachment = self._on_file_upload_request()
                message = ''
            message = self._format_group_message_to_send(message, attachment)
            self.msg_service.send_message(conn, message)
        