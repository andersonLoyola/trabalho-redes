import os
import sys
import time
import socket
from dotenv import load_dotenv
from serializers import WebSocketSerializer, CryptoSerializer
from services import MessagesService, FileStorageService, AuthService, TokenService
from handlers import AuthHandler, CreateChatHandler, GroupChatHandler, ConnectionsHandler, PrivateChatHandler
load_dotenv()

rest_service_host = os.getenv('REST_CLIENT_HOST')
rest_service_api_key = os.getenv('REST_CLIENT_API_KEY')


crypto_serializer = CryptoSerializer()
websocket_serializer = WebSocketSerializer()

auth_service = AuthService(rest_service_host, rest_service_api_key, crypto_serializer)
messages_service = MessagesService(websocket_serializer, crypto_serializer)
token_service = TokenService(crypto_serializer)
filestorage_service=FileStorageService()


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

def show_main_menu():
    while True:
        os.system('cls')
        print('1. Login')
        print('2. Signup')
        print('3. Exit')
        choice = input('Enter choice: ')
        if choice == '1':
            token = auth_handler.handle_login()
            show_chat_options(token)
            os.system('cls')
            break
        elif choice == '2':
            auth_handler.handle_signup()
            os.system('cls')
        elif choice == '3':
            sys.exit()
        else:
            print('Invalid choice')

def show_chat_options(token):
    user_data = {}

    def apply_exponential_backoff(retry_attempt):
        backoff_time = 5 * (2 ** (retry_attempt - 1))
        time.sleep(backoff_time)

    def connect():
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect(('localhost', 9090))
        messages_service.send_handshake_message(conn)
        messages_service.receive_handshake_message(conn)
    
        return conn
    
    def handle_options(conn, user_data):
        print('1. create group chat')
        print('2. list group chats')
        print('3. list available users')
        print('4. Exit')

        choice = input('Enter choice: ')

        if choice == '1':
            create_chat_handler.handle_chat_creation(conn, user_data)
        elif choice == '2':
            group_chat_handler.handle_show_group_chats(conn, user_data)
        elif choice == '3':
            private_chat_handler.handle_show_private_chats(conn, user_data)
        elif choice == '4':
            sys.exit()   
        os.system('cls')

    retry_attempt = 0
    try:
        conn = connect()
        while True:
            user_data = token_service.decode_token(token)
            conn_service = ConnectionsHandler(conn, messages_service)
            conn_service.connection_handler(user_data)
            handle_options(conn, user_data)
            if (retry_attempt >  3):
                break
    except (
        ConnectionResetError, 
        ConnectionAbortedError, 
        ConnectionRefusedError, 
        ConnectionError
    ) as e:
        input(e)
        retry_attempt+=1
        apply_exponential_backoff(retry_attempt)    
    except Exception as e:
        input(e)
    finally:
        auth_service.signoff(user_data['id'], user_data['session_id'])
        messages_service.send_message(conn, { 
            'action': 'disconnect', 
            'user_id': user_data['id'], 
            'session_id': user_data['session_id']
        })
        # ping_pong_thread.join()
    
show_main_menu()