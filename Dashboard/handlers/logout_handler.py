from middlewares.base_handler import SecureHandler
from middlewares.decorators import authentication_required


class LogoutHandler(SecureHandler):
    login_url = '/pyfaas/login'
    def initialize(self, *args, **kwargs):
        super().initialize(*args, **kwargs)
    
    @authentication_required
    def get(self):
        self.auth_middleware.logout()
        return self.redirect(self.login_url)