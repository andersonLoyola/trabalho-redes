import bcrypt 
from flask import jsonify, make_response

class UsersController(): 
    def __init__(self, userRepository, connectionsRepository, jwtService):
        self.jwtService = jwtService
        self.userRepository = userRepository
        self.connectionsRepository = connectionsRepository

    """
        TODO: MAYBE review this logic later, include a device_id in the request to avoid multiple connections
        using the same device    
    """
    def login(self, user_data):
        foundUser = self.userRepository.get_user(user_data['username'])
        if foundUser is None:
            return jsonify({ "message": "user does not exists"}), 404
        if bcrypt.checkpw(user_data['password'].encode('utf-8'), foundUser['password']):
            jwt_tokens = self.jwtService.generate_token(id = str(foundUser['_id']), username = str(foundUser['username']))
            
            response = make_response(jsonify({ 
                "message": "success", 
            }))

            response.set_cookie('refresh_token', jwt_tokens['refresh_token'], httponly=True)
            response.set_cookie('access_token', jwt_tokens['access_token'], httponly=True)

            return response, 200
        return make_response(jsonify({ "message": "username or password does not matches"})), 401
        
    def signup(self, user_data):
        foundUser = self.userRepository.get_user(user_data['username'])
        if foundUser is not None:
            return make_response(jsonify({ "message": "user already exists"})), 409
        user_data['password'] = bcrypt.hashpw(user_data['password'].encode('utf-8'), bcrypt.gensalt())
        self.userRepository.create_user(user_data)
        return make_response(jsonify({ "message": "success"})), 200

    def signoff(self, user_data):
        foundUser = self.userRepository.get_user(user_data['username'])
        if foundUser is None:
            return make_response(jsonify({ "message": "user does not exists"})), 404
        if bcrypt.checkpw(user_data['password'].encode('utf-8'), foundUser['password']):
            return make_response(jsonify({ "message": "username or password does not matches"})), 401
        self.connectionsRepository.delete_connection(user_data['connection_id'])
        return make_response(jsonify({ "message": "success"})), 200
    
    def refresh_token(self, refresh_token):
        try:
            decoded_token = self.jwtService.decode_token(refresh_token)
            foundUser = self.userRepository.get_user(decoded_token['username'])
            
            if foundUser is None:
                return make_response(jsonify({ "message": "user does not exists"})), 404
            jwt_tokens = self.jwtService.generate_token(id = str(foundUser['_id']), username = str(foundUser['username']))
            
            response = make_response(jsonify({ 
                "message": "success",
                }, 
            ))

            response.set_cookie('access_token', jwt_tokens['access_token'], httponly=True)
            response.set_cookie('refresh_token', jwt_tokens['refresh_token'], httponly=True)

            return response, 200
        except Exception as e:
            return jsonify({ "message": "invalid token"}), 401