import json

class ChatController():

    def __init__(
            self, 
            user_connections_repository, 
            messages_repository, 
            websocket_utils_service, 
            jwt_service
        ):
        self.connections = {}
        self.jwt_service = jwt_service
        self.messages_repository = messages_repository
        self.user_connections_repository = user_connections_repository
        self.websocket_utils_service = websocket_utils_service

    
    def load_messages(self, client_socket, sender, receiver):
        messages = self.messages_repository.get_messages(sender, receiver)
        for message in messages:
            client_socket.send(json.dumps(message).encode('utf-8'))


    def receive_message(self, client_socket):
        buffer_size = 1024 # TODO: maybe put this in a config file
        """
            IMPORTANT: this initially has the socket frame parts combined  
            SEE: https://datatracker.ietf.org/doc/html/rfc6455#section-3
        """
        message_parts = bytearray() 
        while True:
            part = client_socket.recv(buffer_size)
            message_parts.extend(part)
            if len(part) < buffer_size:
                break

        message_dict = self.websocket_utils_service.socket_frame_handler(message_parts)     
        
        return message_dict
    
    def handle_client(self,  client_socket):
        self.websocket_utils_service.handshake(client_socket)
        
        decoded_message = self.receive_message(client_socket)

        if not decoded_message['auth_token']:
            client_socket.send('missing token')
            client_socket.close()
            return
        
        try:
            decoded_token = self.jwt_service.verify_token(decoded_message['auth_token'])
        except Exception as e:
            client_socket.send('invalid token')
            client_socket.close()
            return
        
        username = decoded_token['username']
        user_id = decoded_token['user_id']
        user_already_in_chat = self.user_connections_repository.get_user_connections(user_id)           

        # if user is not in the chat we load the previous messages
        # however idk how it should behave if we are joining  a room
        if not user_already_in_chat:
            self.load_messages(client_socket, user_id, user_id)
            return
        
        while True:
            message = self.receive_message(client_socket)
            if not message:
                break
            self.messages_repository.add_message(user_id, user_id, message)
            self.broadcast_message(username, message)
        
        self.user_connections_repository.remove_connection(user_id)
        client_socket.close()
        

    def broadcast_messages(self, user_id, message):
        for connection in self.connections.values():
            connection.send(json.dumps({
                'sender': user_id,
                'message': message
            }).encode('utf-8'))

    def private_messages(self, username, receiver, message, attachments):
        receiver_socket = self.connections.get(receiver)
        
        if not receiver_socket:
            return
        
        receiver_socket.send(json.dumps({
            'sender': username,
            'message': message,
            'attachments': attachments
        }).encode('utf-8'))

    