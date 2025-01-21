import os
import json
"""
    IMPORTANT: this initially has the socket frame parts combined  
    SEE: https://datatracker.ietf.org/doc/html/rfc6455#section-3
"""
class MessagesService(): 

    CHUNK_SIZE = 100 * 1024 # 100 kb
    
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
        msg_bytes = json.dumps(message).encode('utf-8')
        for i in range(0, len(msg_bytes), self.CHUNK_SIZE):
            yield msg_bytes[i:i + self.CHUNK_SIZE] # returns msg bytes from iindex till i index + chunk_size

    def receive_handshake_message(self, receiver_socket ):
        self.websocket_serializer.handshake(receiver_socket)
      
    def receive_message(self, receiver_socket):
        try: 
            message_parts = bytearray()
            done_reading = False
            while done_reading != True:
                part = receiver_socket.recv(self.CHUNK_SIZE)
                if not part:
                    break
                web_socket_frame_data = self.websocket_serializer.decode_socket_frame(part)
                message_parts.extend(web_socket_frame_data['data'])
                done_reading = (web_socket_frame_data['fin'] == 1)
            message = bytes(message_parts).decode('utf-8')
            decrypted_message = self.crypto_serializer.decrypt(json.loads(message))
            return json.loads(decrypted_message)
            
        except Exception as e:
            print(str(e))
            raise e
    
    def send_message(self, receiver_socket, message):
        message_bytes = json.dumps(message).encode('utf-8')
        cyphered_message_bytes = self.crypto_serializer.encrypt(message_bytes)
        message_chunks = list(self._chunk_message(cyphered_message_bytes))
        for i, message_chunk in (enumerate(message_chunks)):
            fin = (i == len(message_chunks) -1)
            encoded_frame = self.websocket_serializer.encode_socket_frame(message_chunk, fin)
            receiver_socket.sendall(encoded_frame)
    
