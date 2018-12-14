import tornado.web
from middlewares.base_handler import SecureHandler

class RegisterHandler(SecureHandler):
    login_url = '/pyfaas/login'

    def initialize(self, *args, **kwargs):
        super().initialize(*args, **kwargs)

    def get(self):
        return self.render('register.html')

    def post(self):
        email = self.get_argument('email')
        password = self.get_argument('password')
        username = self.get_argument('username')
        confirm_password = self.get_argument('confirm_password')

        if password != confirm_password:
            return self.redirect('/pyfaas/register')
        else:
            self.auth_middleware.create_user(email, username, password)
            self.redirect('/pyfaas/upload')