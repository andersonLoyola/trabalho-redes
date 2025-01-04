import os
import socket
from services import MessagesService
from serializers import WebSocketSerializer, CryptoSerializer
from handlers import AuthHandler, CreateChatHandler, ChatOptionHandler, JoinChatHandler


conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect(('localhost', 9090))

messages_service = MessagesService(
    crypto_serializer=CryptoSerializer(),
    websocket_serializer=WebSocketSerializer()
)

messages_service.send_handshake_message(conn)
messages_service.receive_handshake_message(conn)

auth_handler = AuthHandler(conn, messages_service)
create_chat_handler=CreateChatHandler(
    conn=conn,
    msg_service=messages_service
)
chat_options_handler=ChatOptionHandler(
    conn=conn, 
    msg_service=messages_service
) 
join_chat_handler=JoinChatHandler(
    conn=conn,
    msg_service=messages_service,
)
        

while True:
    os.system('cls')
    print('1. Login')
    print('2. Signup')
    print('3. Exit')
    choice = input('Enter choice: ')
    if choice == '1':
        response = auth_handler.handle_login()
        current_user = response['user']
        os.system('cls')
        break
    elif choice == '2':
        response = auth_handler.handle_signup()
        os.system('cls')
    elif choice == '3':
        break
    else:
        print('Invalid choice')


while True:
    print('1. join group chat')
    print('2. create group chat')
    print('3. list group chats')
    print('4. list connected users')
    print('5. create private chat')
    print('6. Exit')

    choice = input('Enter choice: ')
    if choice == '0':
        break
    if choice == '1':
        pass
    elif choice == '2':
        response = create_chat_handler.handle_chat_creation(current_user)
    elif choice == '3':
        current_chat_info=chat_options_handler.handle_chat_options(current_user)
        join_chat_handler.handle_join_group_chat(current_chat_info, current_user)
    elif choice == '4':
        current_chat_info=chat_options_handler.handle_chat_options(current_user)
        join_chat_handler.handle_join_group_chat(current_chat_info, current_user)
    
    os.system('cls')