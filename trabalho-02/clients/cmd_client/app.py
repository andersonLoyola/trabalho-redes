import os
import sys
import time
import socket

from serializers import WebSocketSerializer, CryptoSerializer
from services import MessagesService, FileStorageService, AuthService, TokenService, UserHistoryService
from handlers import AuthHandler, CreateChatHandler, GroupChatHandler, ConnectionsHandler, PrivateChatHandler, UserActivityHandler
import config

crypto_serializer = CryptoSerializer(config.crypto_secret_key)
websocket_serializer = WebSocketSerializer()

filestorage_service=FileStorageService()
token_service = TokenService(crypto_serializer)
messages_service = MessagesService(websocket_serializer, crypto_serializer)
auth_service = AuthService(config.http_server_endpoint, config.http_server_api_key, crypto_serializer)
user_history_service = UserHistoryService(config.http_server_endpoint, config.http_server_api_key, crypto_serializer)

conn_handler = ConnectionsHandler(messages_service)
auth_handler = AuthHandler(auth_service)
create_chat_handler = CreateChatHandler(
    messages_service
)

group_chat_handler = GroupChatHandler(
    messages_service, 
    filestorage_service
)

private_chat_handler = PrivateChatHandler(
    messages_service,
    filestorage_service
)

user_activity_handler = UserActivityHandler(
    user_history_service,
    filestorage_service,
    crypto_serializer
)

def show_main_menu():
    while True:
        os.system('cls')
        print('1. Login')
        print('2. Signup')
        print('3. Exit')
        choice = input('Enter choice: ')
        if choice == '1':
            token = auth_handler.handle_login()
            user_data = token_service.decode_token(token)
            ShowChatOptions(user_data, conn_handler).execute()
            os.system('cls')
            break
        elif choice == '2':
            auth_handler.handle_signup()
            os.system('cls')
        elif choice == '3':
            sys.exit()
        else:
            print('Invalid choice')

class ShowChatOptions:
    conn = None
    user_data = {}
    retry_attempt = 0
    conn_service = {}

    def __init__(self, user_data, conn_service):
        self.user_data = user_data
        self.conn_service = conn_service

    def apply_exponential_backoff(self):
        backoff_time = 10 * (2 ** (self.retry_attempt - 1))
        time.sleep(backoff_time)

    def connect(self):
        while self.retry_attempt <= 3:
            try:
                conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                conn.connect((config.websocket_server_host, config.websocket_server_port))
                messages_service.send_handshake_message(conn)
                messages_service.receive_handshake_message(conn)
                self.conn_service.connection_handler(conn, self.user_data)
                self.retry_attempt = 0  
                return conn
            except (
                ConnectionResetError, 
                ConnectionAbortedError, 
                ConnectionRefusedError, 
                ConnectionError
            ) as e:
                input(str(e))
                self.retry_attempt += 1
                self.apply_exponential_backoff()
        raise Exception("Failed to connect after multiple attempts")
       
    def handle_options(self, conn, user_data):
        while True:
            print('1. create group chat')
            print('2. list group chats')
            print('3. list available users')
            print('4. generate group chat history report')
            print('5. Exit')

            choice = input('Enter choice: ')

            if choice == '1':
                create_chat_handler.handle_chat_creation(conn, user_data)
            elif choice == '2':
                group_chat_handler.handle_show_group_chats(conn, user_data)
            elif choice == '3':
                private_chat_handler.handle_show_private_chats(conn, user_data)
            elif choice == '4':
                user_activity_handler.generate_group_chat_report(user_data)   
            elif choice == '5':
                sys.exit()   
            os.system('cls')

    def execute(self):
        try:
            conn = self.connect()
            self.handle_options(conn, self.user_data)   
        except (
            ConnectionResetError, 
            ConnectionAbortedError, 
            ConnectionRefusedError, 
            ConnectionError
        ) as e:
            conn = self.connect()
            if conn and self.user_data:
                self.handle_options(conn, self.user_data)
        except Exception as e:
            input(str(e))
        finally:
            auth_service.signoff(self.user_data['id'], self.user_data['session_id'])
            messages_service.send_message(conn, { 
                'action': 'disconnect', 
                'user_id': self.user_data['id'], 
                'session_id': self.user_data['session_id']
            })

    
show_main_menu()