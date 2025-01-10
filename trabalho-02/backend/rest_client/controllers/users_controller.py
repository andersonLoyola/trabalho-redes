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
        try:
            request_body = request['body']
            foundUser = self.users_repository.get_user(request_body['username'])
            if foundUser is None:
                return (404, { "message": "user does not exists"})
            if foundUser['password'] == request_body['password']:
                del foundUser['password']
                token = self.token_service.generate_token(foundUser)
                return (
                    200,
                    { 
                        "message": "success", 
                        "token": token,
                    }
                )
            return (401, { "message": "username or password does not matches"})
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

    # def signoff(self, request):
    #     pass

