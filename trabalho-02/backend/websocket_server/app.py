import socket
import threading

from helpers import ActionsQueue
from controllers import ChatController
from serializers import WebSocketSerializer, CryptoSerializer
from services import MessagesService, ConnectionsService, RestService, GroupChatsService 
import config

# ----------------------- SERIALIZERS -----------------------
web_socket_serializer = WebSocketSerializer()
crypto_serializer = CryptoSerializer(config.crypto_secret_key)
# ----------------------- SERVICES ---------------------------
rest_service = RestService(
    config.http_server_api_endpoint,
    config.websocket_server_api_key
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
    server_socket.bind((config.websocket_server_host, int(config.websocket_server_port)))
    server_socket.listen()
    print(f'Server is listening on port {config.websocket_server_port}')

    while True:
        client_socket, addr = server_socket.accept()        
        print(f'Accepted connection from {addr}')
        client_handler = threading.Thread(target=chat_controller.handle_client, args=(client_socket,), name='client_thread')
        client_handler.start()

if __name__ == '__main__':
    start_server()