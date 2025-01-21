class TestRoutes():

    def __init__(self, http_router):
        self.http_router = http_router
        self.set_routes()

    def set_routes(self):
        self.http_router.add_url_rule(
            'dumbus',
            '/api/V1/dumbus',
            'do_something',
            lambda request: (200, {'message': 'hell world'}),
            'POST',
        )