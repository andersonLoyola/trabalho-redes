import os
import jwt
import socket
import threading
from pymongo import MongoClient
from services.jwt_service import JWtService
from controllers.chat_controller import ChatController
from repository.messages_repository import MessagesRepository
from repository.user_connections_repository import UserConnectionsRepository
from services.web_socket_utils import WebSocketUtilsService

mongodb_url = os.getenv('MONGODB_URL')
mongodb_name = os.getenv('MONGODB_NAME')
mongo_client = MongoClient(mongodb_url)
db = mongo_client[mongodb_name]

app_host = os.getenv('chatuba_app_host')
app_port = os.getenv('chatuba_app_port')

secret_key = os.getenv('JWT_SECRET')


user_connections_repository = UserConnectionsRepository(db)
messages_repository = MessagesRepository(db)

jwt_service = JWtService(secret_key, jwt)

websocket_utils_service = WebSocketUtilsService()

chat_controller = ChatController(
    user_connections_repository, 
    messages_repository,
    websocket_utils_service, 
    jwt_service
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