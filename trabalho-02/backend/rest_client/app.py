import os
import jwt
from flask import Flask
from pymongo import MongoClient
from repository import ChatsRepository, UsersRepository, MessagesRepository
from controllers import UsersController, ChatsController
from serializers import ChatSerializer, MessagesSerializer
from routes import UserRoutes, ChatsRoutes
from services import JwtService
from routes import ChatsRoutes
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


jwt_secret = os.getenv('jwt_secret')
mongo_uri = os.getenv('mongo_uri')
app_host = os.getenv('chatuba_app_host')
app_port = os.getenv('chatuba_app_port')

chatuba_webclient_host = os.getenv('chatuba_webclient_host')

cors = CORS(app, resources={r"/api/*": {"origins": [ chatuba_webclient_host ] }}) # TODO: move it to a config file later

mongo_client = MongoClient(mongo_uri)
db = mongo_client['chatuba']

jwtService = JwtService(jwt, jwt_secret)

messagesRepository = MessagesRepository(db)
messagesSerializer = MessagesSerializer()

userRepository = UsersRepository(db)
usersController = UsersController(userRepository, jwtService)
userRoutes = UserRoutes(app, usersController)

chatsRepository = ChatsRepository(db)
chatsSerializer = ChatSerializer()
chatsController = ChatsController(
    jwtService, 
    chatsRepository, 
    messagesRepository, 
    userRepository, 
    chatsSerializer,
    messagesSerializer,
)
chatsRoutes = ChatsRoutes(app, chatsController)




if __name__ == '__main__':
    with app.test_request_context():
        for rule in app.url_map.iter_rules():
            print(f"{rule.endpoint}: {rule}")

    app.run(host=app_host, port=app_port)

