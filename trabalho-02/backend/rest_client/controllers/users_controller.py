import uuid
import traceback

class UsersController: 
    def __init__(
            self, 
            users_repository,   
            crypto_serializer,
            token_service,
        ):
        self.token_service = token_service
        self.users_repository = users_repository
        self.crypto_serializer = crypto_serializer

    def login(self, request):
        session_id =  ''
        try:
            request_body = request['body']
            foundUser = self.users_repository.get_user(request_body['username'])
            if foundUser is None:
                return (404, { "message": "user does not exists"})
            if foundUser['password'] != request_body['password']:
                return (401, { "message": "username or password does not matches"})
            del foundUser['password']
            user_sessions = self.users_repository.count_user_sessions(foundUser['id'])
            found_available_session = self.users_repository.find_inactive_sessions(foundUser['id'])
            if found_available_session == None and user_sessions['sessions_count'] >= 3:
                return (401, { "message": 'too many active sessions' })
            elif found_available_session != None:
                session_id = found_available_session['session_id']
                self.users_repository.update_user_session_status(foundUser['id'], session_id, 'ACTIVE')
            else:
                session_id = self.users_repository.create_user_session(foundUser['id'], str(uuid.uuid4()))
            foundUser['session_id'] = session_id
            token = self.token_service.generate_token(foundUser)
            return (
                200,
                { 
                    "message": "success", 
                    "token": token,
                }
            )
        except Exception as e:
            print(e)
            traceback.print_exc()
    
    def signup(self, request):
        try:
            request_body = request['body']
            foundUser = self.users_repository.get_user(request_body['username'])
            if foundUser is not None:
                return 409, { "message": "user already exists"}
            self.users_repository.create_user(request_body)
            return 201, { "message": "success"}
        except Exception as e:
            print(e)
            traceback.print_exc()

    def signoff(self, request):
        try:
            token = request['headers'].get('Authorization').split(' ')[-1]
            request_body = request['body']
            decoded_token = self.token_service.decode_token(token)
            if (not decoded_token or 'id' not in decoded_token or 'session_id' not in decoded_token):
                return 401, {'message': 'unauthorized'}
            found_user = self.users_repository.find_user_by_session_id(request_body['session_id'])
            if not found_user:
                return 404, {'message': 'user not found'}
            self.users_repository.update_user_session_status(request_body['user_id'], request_body['session_id'], 'INACTIVE')
            return 200, {'message': 'signedoff successfully'}
        except Exception as e:
            print(e)
            traceback.print_exc()

