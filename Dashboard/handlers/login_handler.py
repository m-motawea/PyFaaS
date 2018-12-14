import tornado.web
from middlewares.base_handler import SecureHandler

class LoginHandler(SecureHandler):
    login_url = '/pyfaas/login'
    def initialize(self, *args, **kwargs):
        super().initialize(*args, **kwargs)
        
    def get(self):
        self.render('login.html')

    def post(self):
        email = self.get_argument('email')
        password = self.get_argument('password')
        user = self.auth_middleware.check_user(email, password)
        if user:
            self.auth_middleware.login(user)
            return self.redirect('/pyfaas/functions')
        else:
            return self.redirect(self.login_url)