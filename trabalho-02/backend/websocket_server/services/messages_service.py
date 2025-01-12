import json
import traceback

class MessagesService(): 

    def __init__(
            self,      
            websocket_serializer, 
            crypto_serializer,
            actions_queue,
            rest_service,
        ):
        self.rest_service = rest_service
        self.actions_queue = actions_queue
        self.crypto_serializer = crypto_serializer
        self.websocket_serializer = websocket_serializer

    def _chunk_message(self, message):
        chunk_size = 1024 * 256 # 1/4 or mb
        msg_bytes = json.dumps(message).encode('utf-8')
        for i in range(0, len(msg_bytes), chunk_size):
            yield msg_bytes[i:i + chunk_size] # returns msg bytes from iindex till i index + chunk_size

  
    def receive_handshake_message(self, receiver_socket):
        try:
            self.websocket_serializer.handshake(receiver_socket)
        except Exception as e:
            traceback.print_exc()
            print(e)
    
    def receive_message(self, receiver_socket):
        try:
            buffer_size = 1024 * 256 # TODO: maybe put this in a config file
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

            encrypted_message = self.websocket_serializer.decode_socket_frame(message_parts)     
            decrypted_message = self.crypto_serializer.decrypt(encrypted_message)
            return json.loads(decrypted_message)
        except Exception as e:
            traceback.print_exc()
            print(e)
            raise e

    def send_message(self, receiver_socket, message):
        try:
            message_bytes = json.dumps(message).encode('utf-8')
            cyphered_message_bytes = self.crypto_serializer.encrypt(message_bytes)
            message_chunks = list(self._chunk_message(cyphered_message_bytes))
            for i, message_chunk in (enumerate(message_chunks)):
                fin = (i == len(message_chunks) -1)
                encoded_frame = self.websocket_serializer.encode_socket_frame(message_chunk, fin)
                receiver_socket.send(encoded_frame)
        except Exception as e:
            traceback.print_exc()
            print(e)
            raise e