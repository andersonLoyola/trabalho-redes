import json
import base64

class TokenService: 

    def __init__(self, crypto_serializer):
        self.crypto_serializer = crypto_serializer

    def generate_token(self, user_data):
        try:
            user_data_bytes = json.dumps(user_data).encode('utf-8')
            token = self.crypto_serializer.encrypt(user_data_bytes)
            return base64.b64encode(json.dumps(token).encode('utf-8')).decode('utf-8')
        except Exception as e:
            print(e)
            

    def decode_token(self, token):
        try:
            decompressed_token = base64.b64decode(token).decode('utf-8')
            decompressed_token = json.loads(decompressed_token)
            user_data = self.crypto_serializer.decrypt(decompressed_token)
            return json.loads(user_data)
        except Exception as e:
            print(e)