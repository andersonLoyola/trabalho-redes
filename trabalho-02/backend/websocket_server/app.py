import os
import socket
import threading
from dotenv import load_dotenv

from helpers import ActionsQueue
from controllers import ChatController
from serializers import WebSocketSerializer, CryptoSerializer
from services import MessagesService, ConnectionsService, RestService, GroupChatsService 

load_dotenv()

secret_key = os.getenv('SECRET_KEY')
api_endpoint= os.getenv('api_endpoint')
api_key = os.getenv('api_key')
app_host = os.getenv('chatuba_app_host')
app_port = os.getenv('chatuba_app_port')

# ----------------------- SERIALIZERS -----------------------
web_socket_serializer = WebSocketSerializer()
crypto_serializer = CryptoSerializer(secret_key)
# ----------------------- SERVICES ---------------------------
rest_service = RestService(
    api_endpoint,
    api_key
)
actions_queue = ActionsQueue(
    rest_service,
    crypto_serializer
)
connections_service = ConnectionsService.get_instance(rest_service)
messages_service = MessagesService(
    web_socket_serializer, 
    crypto_serializer, 
    actions_queue,
)
group_chats_service = GroupChatsService(
    actions_queue,
    rest_service
)
# ----------------------- dedicated thread to run specific operations ------
actions_queue_thread = threading.Thread(target=actions_queue.run, name= 'actions_queue',daemon=True)
actions_queue_thread.start()
# ----------------------- CONTROLLERS ------------------------
chat_controller = ChatController(
    actions_queue, 
    connections_service, 
    messages_service,
    group_chats_service
)
 # --------------------- loads group chats from database ------------
group_chats_service.load_group_chats_from_service()    
# ----------------------- handler init -----------------------
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((app_host, int(app_port)))
    server_socket.listen()
    print(f'Server is listening on port {app_port}')

    while True:
        client_socket, addr = server_socket.accept()        
        print(f'Accepted connection from {addr}')
        client_handler = threading.Thread(target=chat_controller.handle_client, args=(client_socket,), name='client_thread')
        client_handler.start()

if __name__ == '__main__':
    start_server()