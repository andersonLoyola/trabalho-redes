from flask import jsonify
from jwt  import InvalidTokenError, ExpiredSignatureError

class ConnectionsController():

    def  __init__(self, jwtService, connectionsRepository):
        self.jwtService = jwtService
        self.connectionsRepository = connectionsRepository

    def create_group_connection(self, connection_data):
        try:
            self.jwtService.decode_token(connection_data['access_token'])
            self.connectionsRepository.create_group_connection(connection_data)
            return jsonify({ "message": "success"}), 200
        except ExpiredSignatureError:
            return jsonify({"message": "token has expired"}), 401
        except InvalidTokenError:
            return jsonify({"message": "invalid token"}), 401
        except Exception:
            return jsonify({"message": "internal server error"}), 500
        


   