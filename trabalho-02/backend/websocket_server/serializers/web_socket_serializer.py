import json
import base64
import hashlib

class WebSocketSerializer():

    FIN_EXTRACTION_MASK = 0b10000000 
    MASK_EXTRACTION_BYTE = 0b10000000
    OPCODE_EXTRACTION_MASK = 0b00001111
    PAYLOAD_LENGTH_EXTRACTION_BYTE = 0b01111111 

    """
    'GET / HTTP/1.1\r\n
    Host: localhost:9090\r\n
    Connection: Upgrade\r\n
    Pragma: no-cache\r\nCache-Control: no-cache\r\n
    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36\r\n
    Upgrade: websocket\r\n
    Origin: null\r\nSec-WebSocket-Version: 13\r\n
    Accept-Encoding: gzip, deflate, br, zstd\r\n
    Accept-Language: pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7\r\n
    Sec-WebSocket-Key: TZ/zHeAVk15vOSYhxVs8rA==\r\n
    Sec-WebSocket-Extensions: permessage-deflate; client_max_window_bits\r\n
    \r\n'

    """
    def parse_headers(self, request):
        headers = {}
        request_chunks = request.split('\r\n')
        for chunk in request_chunks[1:]:
            if chunk:
                key, value = chunk.split(': ', 1)
                headers[key] = value
        return headers

    def handshake(self, client_socket):
        request = client_socket.recv(1024).decode('utf-8')
        headers = self.parse_headers(request)
        websocket_key = headers['Sec-WebSocket-Key']
        websocket_accept = base64.b64encode(hashlib.sha1((websocket_key + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11').encode('utf-8')).digest()).decode('utf-8')
        response = (
            'HTTP/1.1 101 Switching Protocols\r\n'
            'Upgrade: websocket\r\n'
            'Connection: Upgrade\r\n'
            f'Sec-WebSocket-Accept: {websocket_accept}\r\n\r\n'
        )
        client_socket.send(response.encode('utf-8'))


    """
        from: https://datatracker.ietf.org/doc/html/rfc6455#section-5.1
        and: https://datatracker.ietf.org/doc/html/rfc6455#section-5.2 
        NOTE: we ae working with bytearrays here, so each index equals to a 
        byte  
    """    
    def decode_socket_frame(self, data):
        first_byte = data[0]
        """ 
            bitwise  if both bits are 1 then i returns 1 else returns 0. 
            It is being done to get the FIN bit from the websocket protocol, attained 
            by isolating the most significant bit
            FIN BIT, used to know wether this frame is a continuation frame or not
        """
        fin = first_byte & self.FIN_EXTRACTION_MASK # TODO: SEE WHY THIS IS NOT BEING USED

        """
        
        """
        opcode = first_byte & self.OPCODE_EXTRACTION_MASK #opcode
        if opcode == 8: # TODO: SEE WHY IN THE DOCS LATER
            return None
        
        second_byte = data[1]
        mask = second_byte & self.MASK_EXTRACTION_BYTE # TODO: SEE WHY THIS IS NOT BEING USED
        payload_length = second_byte & self.PAYLOAD_LENGTH_EXTRACTION_BYTE

        """
            PER: https://datatracker.ietf.org/doc/html/rfc6455#section-3
            WHEN: payload_length  is within 0-125 
                THEN: this is the payload length
            WHEN: payload_length is 126:
                THEN: the next 2 bytes must be interpreted as a 16-bit unsigned interger
                AND: they are the payload length
            WHEN: payload_length is 127:
                THEN: the most significant bit must be 0
                AND: the following 8 bytes must be interpreted as a 64-bit unsigned
                    integer, and they must be interpreted as the payload length
        """
        if payload_length == 126:
            extended_payload_length = data[2:4] 
            # we use byteorder big here cause the MSB is in the beginning of the array
            payload_length = int.from_bytes(extended_payload_length, byteorder='big')
            masking_key = data[4:8]
            payload_data = data[8:]
        elif payload_length == 127:
            extended_payload_length =data[2:10]
            # we use byteorder big here cause the MSB is in the beginning of the array
            payload_length = int.from_bytes(extended_payload_length, byteorder='big')
            masking_key = data[10:14]
            payload_data = data[14: ]
        else:
            masking_key = data[2:6] # 
            payload_data = data[6:] # takes the other bits as the data
        # TODO: REWRITE THIS LATER
        message_bytes = bytearray([payload_data[i] ^ masking_key[i % 4] for i in range(payload_length)])
        message = message_bytes.decode('utf-8')
        return json.loads(message)
    """
        https://stackoverflow.com/questions/8125507/how-can-i-send-and-receive-websocket-messages-on-the-server-side
        https://stackoverflow.com/questions/40664747/python-encode-web-socket-frames
    """
    def encode_socket_frame(self, message):
        raw_binary_message = json.dumps(message).encode('utf-8')
    
        bytesFormatted = []
        bytesFormatted.append(129)

        bytesLength = len(raw_binary_message)
        if bytesLength <= 125 :
            bytesFormatted.append(bytesLength)
        elif bytesLength >= 126 and bytesLength <= 65535 :
            bytesFormatted.append(126)
            bytesFormatted.append( ( bytesLength >> 8 ) & 255 )
            bytesFormatted.append( bytesLength & 255 )
        else :
            bytesFormatted.append( 127 )
            bytesFormatted.append( ( bytesLength >> 56 ) & 255 )
            bytesFormatted.append( ( bytesLength >> 48 ) & 255 )
            bytesFormatted.append( ( bytesLength >> 40 ) & 255 )
            bytesFormatted.append( ( bytesLength >> 32 ) & 255 )
            bytesFormatted.append( ( bytesLength >> 24 ) & 255 )
            bytesFormatted.append( ( bytesLength >> 16 ) & 255 )
            bytesFormatted.append( ( bytesLength >>  8 ) & 255 )
            bytesFormatted.append( bytesLength & 255 )

        bytesFormatted = bytes(bytesFormatted)
        bytesFormatted = bytesFormatted + raw_binary_message
        return bytesFormatted