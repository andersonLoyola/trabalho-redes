
class UsersController(): 
    def __init__(self, userRepository, jwtService):
        self.jwtService = jwtService
        self.userRepository = userRepository

    """
        TODO: MAYBE review this logic later, include a device_id in the request to avoid multiple connections
        using the same device    
    """
    def login(self, request):

        request_body = request['body']
        foundUser = self.userRepository.get_user(request_body['username'])
        if foundUser is None:
            return (404, { "message": "user does not exists"})
        if foundUser['password'] == request_body['password']:
            jwt_tokens = self.jwtService.generate_token(id = str(foundUser['id']), username = str(foundUser['username']))
            return (
                200,
                { 
                    "message": "success", 
                    "access_token": jwt_tokens['access_token'],
                    "refresh_token": jwt_tokens['refresh_token'],
                }
            )
        return (401, { "message": "username or password does not matches"})
        
    def signup(self, request):
        request_body = request['body']
        foundUser = self.userRepository.get_user(request_body['username'])
        if foundUser is not None:
            return 409, { "message": "user already exists"}
        self.userRepository.create_user(request_body)
        return 201, { "message": "success"}

    def signoff(self, request):
        return 200, {'message': 'worked'}

    def refresh_token(self, request):
        return 200, {'message': 'worked'}