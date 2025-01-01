import os
import jwt
import socket
import threading
from pymongo import MongoClient
from services import JWtService, MessagesService, FileStorageService 
from serializers import WebSocketSerializer
from repository import ChatsRepository, MessagesRepository, UserConnectionsRepository
from controllers import ChatController

mongodb_url = os.getenv('MONGODB_URL')
mongodb_name = os.getenv('MONGODB_NAME')
mongo_client = MongoClient(mongodb_url)
db = mongo_client[mongodb_name]

app_host = os.getenv('chatuba_app_host')
app_port = os.getenv('chatuba_app_port')

secret_key = os.getenv('JWT_SECRET')

web_socket_serializer = WebSocketSerializer()

chats_repository = ChatsRepository(db)
messages_repository = MessagesRepository(db)
user_connections_repository = UserConnectionsRepository(db)

jwt_service = JWtService(secret_key, jwt)
web_socket_serializer = WebSocketSerializer()
messages_service = MessagesService(messages_repository, web_socket_serializer)
file_storage_service = FileStorageService(app_host, app_port)
chat_controller = ChatController(
    chats_repository,
    messages_service,
    jwt_service,
    file_storage_service,
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