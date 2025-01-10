import os
import sys
import uuid
import socket
from serializers import WebSocketSerializer, CryptoSerializer
from handlers import AuthHandler, CreateChatHandler, ChatOptionHandler, GroupChatHandler, ConnectionsHandler
from services import MessagesService, FileStorageService, ChatubaApiService, TokenService




chatuba_api_service = ChatubaApiService('http://localhost:8080/api/v1')

crypto_serializer = CryptoSerializer()
websocket_serializer = WebSocketSerializer()

messages_service = MessagesService(
    websocket_serializer,
    crypto_serializer,
)

token_service = TokenService(crypto_serializer)

filestorage_service=FileStorageService()

auth_handler = AuthHandler(
    chatuba_api_service, 
)

create_chat_handler=CreateChatHandler(
  chat_api=chatuba_api_service
)
chat_options_handler=ChatOptionHandler(
    chatuba_api=chatuba_api_service
) 


group_chat_handler=GroupChatHandler(
    token_service=token_service,
    msg_service=messages_service,
    file_storage_service=filestorage_service
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
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect(('localhost', 9090))
    # --- do handshake ---
    messages_service.send_handshake_message(conn)
    user_data = token_service.decode_token(token)
    messages_service.receive_handshake_message(conn)
    # -- tries to connct ---
    conn_service = ConnectionsHandler(conn, messages_service)
    conn_service.connection_handler(user_data)

    while True:
        print('1. create group chat')
        print('2. list group chats')
        print('3. list available users')
        print('6. Exit')

        choice = input('Enter choice: ')
    
        if choice == '1':
            create_chat_handler.handle_chat_creation(token)
        elif choice == '2':
            chat_info = chat_options_handler.handle_group_chats_options(token)
            group_chat_handler.handle_join_group_chat(conn, chat_info, token)
        elif choice == '3':
            pass
            # current_chat_info=chat_options_handler.handle_available_users_chats(current_user)
            # group_chat_handler.handle_join_private_chat(current_chat_info, current_user)
        
        os.system('cls')


show_main_menu()