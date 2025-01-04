import threading
from .base_handler import BaseHandler

class JoinChatHandler(BaseHandler):
    def __init__(self, conn, msg_service):
        self.conn =  conn
        self.msg_service = msg_service
        self.current_user_info = {}
        self.current_chat_info = {}
    
    def _route_messages():
        pass
    
    # probably there is a bteer way but i'm tired of rthis shit
    def _format_message_to_send(self, message, attachment):
        if attachment:
             return {
                'send_name': self.current_user_info['username'],
                'sender_id': self.current_user_info['user_id'],
                'chat_id': self.current_chat_info['chat_id'],
                'request_type': 'message',
                'attachment': attachment,
                'message': message,
            }
        
        return {
            'sender_id': self.current_user_info['user_id'],
            'sender': self.current_user_info['username'],
            'chat_id': self.current_chat_info['chat_id'],
            'request_type':  'message',
            'message': message,
            'attachment': ''
        }
    
    def _format_received_message(self, message):
        if not message['attachment']:
            return f'{message['sender']}> {message['message']}'

    def _format_private_message(self, message):
        pass

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
            message = self._format_message_to_send(f'{self.current_user_info['username']} has joined the chat', '')
            self.msg_service.send_message(self.conn, message)
        elif 'error' in response:
            self.handle_error(response['error'], 'JOINING CHAT CONNECTION')
    def _handle_received_messages(self):
        response = self.msg_service.receive_message(self.conn)
        if response != None and response['response_type'] == 'message':
            if 'chat_id' in response and self.current_chat_info['chat_id'] == response['chat_id']:
                formatted_message = self._format_received_message(response)
                print(f'\n{formatted_message}')
                print("> ", flush=True)

    def _handle_disconnect_from_chat():
        pass

    def handle_join_group_chat(self, chat_info, current_user_info):
        self.current_user_info = current_user_info
        self.current_chat_info = chat_info
        self._on_join_group_chat_message()
        receive_messages_thread = threading.Thread(target=self._handle_received_messages, daemon=True)
        receive_messages_thread.start()
        while True:
            message = input("> ")
            if input == '\\q':
                break
            message = self._format_message_to_send(message, '')
            self.msg_service.send_message(self.conn, message)

        
    

    def handle_join_user_chat(self, chat_info):
        pass 