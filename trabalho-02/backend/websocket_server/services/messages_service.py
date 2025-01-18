import json

class MessagesService(): 

    def __init__(
            self,      
            websocket_serializer, 
            crypto_serializer,
            actions_queue,
        ):
        self.actions_queue = actions_queue
        self.crypto_serializer = crypto_serializer
        self.websocket_serializer = websocket_serializer
     
    def _chunk_message(self, message):
        chunk_size = 1024 * 256 # 1/4 or mb
        msg_bytes = json.dumps(message).encode('utf-8')
        for i in range(0, len(msg_bytes), chunk_size):
            yield msg_bytes[i:i + chunk_size] # returns msg bytes from iindex till i index + chunk_size

  
    def receive_handshake_message(self, receiver_socket, ):
        self.websocket_serializer.handshake(receiver_socket)
      

    def receive_message(self, receiver_socket):
        buffer_size = 1024 * 256 # TODO: maybe put this in a config file
        """
            IMPORTANT: this initially has the socket frame parts combined  
            SEE: https://datatracker.ietf.org/doc/html/rfc6455#section-3
        """
        message_parts = bytearray() 
        while True:
            part = receiver_socket.recv(buffer_size)
            decoded_frame = self.websocket_serializer.decode_socket_frame(part)     
            message_parts.extend(decoded_frame)
            if len(part) < buffer_size:
                break
        message = message_parts.decode('utf-8')
        decrypted_message = self.crypto_serializer.decrypt(json.loads(message))
        return json.loads(decrypted_message)

    def send_message(self, receiver_socket, message):
        message_bytes = json.dumps(message).encode('utf-8')
        cyphered_message_bytes = self.crypto_serializer.encrypt(message_bytes)
        message_chunks = list(self._chunk_message(cyphered_message_bytes))
        for i, message_chunk in (enumerate(message_chunks)):
            fin = (i == len(message_chunks) -1)
            encoded_frame = self.websocket_serializer.encode_socket_frame(message_chunk, fin)
            receiver_socket.send(encoded_frame)
        