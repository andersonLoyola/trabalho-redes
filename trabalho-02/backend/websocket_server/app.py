import os
import socket
import threading
import sqlite3
from dotenv import load_dotenv

from database import ConnectionPool
from controllers import ChatController
from serializers import WebSocketSerializer, CryptoSerializer
from repository import ChatsRepository, MessagesRepository, UsersRepository
from services import MessagesService, FileStorageService, AuthService, ConnectionsService 

load_dotenv()


secret_key = os.getenv('SECRET_KEY')
app_host = os.getenv('chatuba_app_host')
app_port = os.getenv('chatuba_app_port')
chatuba_db = os.getenv('chatuba_db_path')
connection_pool = ConnectionPool(chatuba_db)


def _init_web_socket_server(client_socket):
    # ----------------------- SERIALIZERS -----------------------
    web_socket_serializer = WebSocketSerializer()
    crypto_serializer = CryptoSerializer(secret_key)
    # ----------------------- REPOSITORIES -----------------------    
    chats_repository = ChatsRepository(connection_pool)
    messages_repository = MessagesRepository(connection_pool)
    users_repository = UsersRepository(connection_pool)
    # ----------------------- SERVICES ---------------------------
    auth_service = AuthService(users_repository)
    file_storage_service = FileStorageService(app_host, app_port)
    messages_service = MessagesService(messages_repository, web_socket_serializer, crypto_serializer)
    connections_service = ConnectionsService.get_instance(chats_repository)
    # ----------------------- CONTROLLERS ------------------------
    chat_controller = ChatController(auth_service, connections_service, file_storage_service, messages_service)
    # ----------------------- handler init -----------------------
    chat_controller.handle_client(client_socket)


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((app_host, int(app_port)))
    server_socket.listen()
    print(f'Server is listening on port {app_port}')

    while True:
        client_socket, addr = server_socket.accept()        
        print(f'Accepted connection from {addr}')
        client_handler = threading.Thread(target=_init_web_socket_server, args=(client_socket,))
        client_handler.start()

if __name__ == '__main__':
    start_server()