
class MessagesService(): 

    def __init__(self, chat_message_repository, websocket_serializer):
        self.chat_message_repository = chat_message_repository
        self.websocket_serializer = websocket_serializer

    def store_messages(self, sender, receiver, message, attachment):
        self.chat_message_repository.create_message(sender, receiver, message, attachment)
      
    def receive_message(self, receiver_socket):
        buffer_size = 1024 # TODO: maybe put this in a config file
        """
            IMPORTANT: this initially has the socket frame parts combined  
            SEE: https://datatracker.ietf.org/doc/html/rfc6455#section-3
        """
        message_parts = bytearray() 
        while True:
            part = receiver_socket.recv(buffer_size)
            message_parts.extend(part)
            if len(part) < buffer_size:
                break

        message_dict = self.websocket_serializer.decode_socket_frame(message_parts)     
        
        return message_dict

    def receive_handshake_message(self, receiver_socket):
        self.websocket_serializer.handshake(receiver_socket)

    def send_message(self, receiver_socket, message):
        encoded_frame = self.websocket_serializer.encode_socket_frame(message)
        receiver_socket.send(encoded_frame)