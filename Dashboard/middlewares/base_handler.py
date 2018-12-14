import tornado.web
from middlewares.jwt_auth import JWTMiddleware
from middlewares.session_auth import SessionMiddleware

class SecureHandler(tornado.web.RequestHandler):
    login_url = '/login'

    def initialize(self, config, session=False, jwt=False, *args, **kwargs):
        self.conf = config
        self.auth_middleware = None
        self.user = None
        session_flag = session
        jwt_flag = jwt

        if not session_flag and not jwt_flag:
            return
        if session_flag and jwt_flag:
            raise Exception("you can either set session or jwt for authentication. you can't use them both!")
        if session_flag:
            self.auth_middleware = SessionMiddleware(self, self.conf)
        if jwt_flag:
            self.auth_middleware = JWTMiddleware(self, self.conf)
