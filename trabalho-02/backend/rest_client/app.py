"""
This should import the routes an then create and initialize a flask application
the port and the host should be  attained via environment variables
"""
import os
import jwt
from flask import Flask
from pymongo import MongoClient
from routes.user_routes import UserRoutes
from repository.users_repository import UsersRepository
from services.jwt_service import JwtService
from controllers.users_controller import UsersController
from repository.connections_repository import ConnectionsRepository
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

cors = CORS(app, resources={r"/api/*": {"origins": "http://localhost:3001"}}) # TODO: move it to a config file later

jwt_secret = os.getenv('jwt_secret')
mongo_uri = os.getenv('mongo_uri')
app_host = os.getenv('chatuba_app_host')
app_port = os.getenv('chatuba_app_port')

mongo_client = MongoClient(mongo_uri)
db = mongo_client['chatuba']

jwtService = JwtService(jwt, jwt_secret)
userRepository = UsersRepository(db)
connectionsRepository = ConnectionsRepository(db)
usersController = UsersController(userRepository, connectionsRepository,jwtService)
userRoutes = UserRoutes(app, usersController)

if __name__ == '__main__':
    app.run(host=app_host, port=app_port)

