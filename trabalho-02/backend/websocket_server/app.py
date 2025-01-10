import os
import socket
import threading
from dotenv import load_dotenv

from helpers import ActionsQueue
from controllers import ChatController
from serializers import WebSocketSerializer, CryptoSerializer
from services import MessagesService, ConnectionsService, RestService 

load_dotenv()

secret_key = os.getenv('SECRET_KEY')
app_host = os.getenv('chatuba_app_host')
app_port = os.getenv('chatuba_app_port')
chatuba_db = os.getenv('chatuba_db_path')
websocket_token = os.getenv('websocket_token')
api_endpoint= os.getenv('API_ENDPOINT')

rest_service = RestService.get_instance(api_endpoint, websocket_token)
connections_service = ConnectionsService.get_instance(rest_service)
actions_queue = ActionsQueue.get_instance(rest_service)
# ----------------------- dedicated thread to run specific operations ------
actions_queue_thread = threading.Thread(target=actions_queue.run, daemon=True)
actions_queue_thread.start()


def _init_web_socket_server(client_socket):
    # ----------------------- SERIALIZERS -----------------------
    web_socket_serializer = WebSocketSerializer()
    crypto_serializer = CryptoSerializer(secret_key)
    # ----------------------- SERVICES ---------------------------
    messages_service = MessagesService(
        web_socket_serializer, 
        crypto_serializer, 
        actions_queue, 
        rest_service
    )
    # ----------------------- CONTROLLERS ------------------------
    chat_controller = ChatController(actions_queue, connections_service, messages_service)
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