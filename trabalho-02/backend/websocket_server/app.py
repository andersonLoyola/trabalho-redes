import os
import socket
import threading
from dotenv import load_dotenv

from services import MessagesService, FileStorageService, AuthService, ConnectionsService 
from serializers import WebSocketSerializer, CryptoSerializer
from repository import ChatsRepository, MessagesRepository, UsersRepository
from controllers import ChatController

load_dotenv()

chatuba_db = os.getenv('chatuba_db_path')

app_host = os.getenv('chatuba_app_host')
app_port = os.getenv('chatuba_app_port')

secret_key = os.getenv('JWT_SECRET')



web_socket_serializer = WebSocketSerializer()

chats_repository = ChatsRepository(chatuba_db)
messages_repository = MessagesRepository(chatuba_db)
users_repository = UsersRepository(chatuba_db)

auth_service = AuthService(users_repository)
web_socket_serializer = WebSocketSerializer()
crypto_serializer = CryptoSerializer('TXshgL49Sfj0GXjEU7IWjpY/9+pVHAmD3eW/29hRK1U=')

file_storage_service = FileStorageService(app_host, app_port)

chat_controller = ChatController(
    auth_service=AuthService(users_repository),
    connections_service=ConnectionsService(chats_repository),
    file_storage_service=FileStorageService(app_host, app_port),
    messages_service=MessagesService(
        messages_repository, 
        web_socket_serializer,
        crypto_serializer,
    ),
)

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((app_host, int(app_port)))
    server_socket.listen()
    print(f'Server is listening on port {app_port}')

    while True:
        client_socket, addr = server_socket.accept()        
        print(f'Accepted connection from {addr}')
        client_handler = threading.Thread(target=chat_controller.handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == '__main__':
    start_server()