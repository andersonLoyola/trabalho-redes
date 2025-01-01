import bcrypt 
from flask import jsonify

class UsersController(): 
    def __init__(self, userRepository, jwtService):
        self.jwtService = jwtService
        self.userRepository = userRepository

    """
        TODO: MAYBE review this logic later, include a device_id in the request to avoid multiple connections
        using the same device    
    """
    def login(self, request):

        request_body = request.get_json()
        foundUser = self.userRepository.get_user(request_body['username'])
        if foundUser is None:
            return jsonify({ "message": "user does not exists"}), 404
        if bcrypt.checkpw(request_body['password'].encode('utf-8'), foundUser['password']):
            
            jwt_tokens = self.jwtService.generate_token(id = str(foundUser['_id']), username = str(foundUser['username']))
            
            return jsonify({ 
                "message": "success", 
                "access_token": jwt_tokens['access_token'],
                "refresh_token": jwt_tokens['refresh_token'],
            }), 200
        return jsonify({ "message": "username or password does not matches"}), 401
        
    def signup(self, request):
        request_body = request.get_json()
        foundUser = self.userRepository.get_user(request_body['username'])
        if foundUser is not None:
            return jsonify({ "message": "user already exists"}), 409
        request_body['password'] = bcrypt.hashpw(request_body['password'].encode('utf-8'), bcrypt.gensalt())
        self.userRepository.create_user(request_body)
        return jsonify({ "message": "success"}), 200

    def signoff(self, request):
        request_body = request.get_json()
        foundUser = self.userRepository.get_user(request_body['username'])
        if foundUser is None:
            return jsonify({ "message": "user does not exists"}), 404
        if bcrypt.checkpw(request_body['password'].encode('utf-8'), foundUser['password']):
            return jsonify({ "message": "username or password does not matches"}), 401
        
        return jsonify({ "message": "success"}), 200

    def refresh_token(self, request):
        request_body = request.get_json()
        try:
            decoded_token = self.jwtService.decode_token(request_body['refresh_token'])
            foundUser = self.userRepository.get_user(decoded_token['username'])
            
            if foundUser is None:
                return jsonify({ "message": "user does not exists"}), 404
            
            jwt_tokens = self.jwtService.generate_token(id = str(foundUser['_id']), username = str(foundUser['username']))
            
            
            return jsonify({ 
                "message": "success",
                'access_token': jwt_tokens['access_token'],
                'refresh_token': jwt_tokens['refresh_token'],
            }), 200

        except Exception as e:
            return jsonify({ "message": "invalid token"}), 401