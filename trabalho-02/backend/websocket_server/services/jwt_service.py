class JWtService():

    def __init__(self, secret_key, jwt_client):
        self.secret_key = secret_key
        self.algorithm = 'HS256'
        self.jwt_client = jwt_client
    
    def decode_token(self, token):
        return self.jwt_client.decode(token, self.secret_key, algorithms=[self.algorithm])