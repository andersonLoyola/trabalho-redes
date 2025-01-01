import datetime



class JwtService():
    
    def __init__(self, jwt_client, jwt_secret):
        self.jwt_client = jwt_client
        self.jwt_secret = jwt_secret
    
    def generate_token(self, id, username):
        
        access_token = self.jwt_client.encode({ 
            "user_id": id, 
            'username': username,
            'exp' : datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=120)
        }, self.jwt_secret, algorithm='HS256')
        
        refresh_token = self.jwt_client.encode({ 
            "user_id": id, 
            'username': username,
            'exp' : datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7),
            
        }, self.jwt_secret, algorithm='HS256')

        return { "access_token": access_token, "refresh_token": refresh_token }


    def decode_token(self, token):
        return self.jwt_client.decode(token, self.jwt_secret, algorithms=['HS256'])