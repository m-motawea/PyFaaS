from middlewares.base_handler import SecureHandler
from middlewares.decorators import authentication_required
from models.functions import Function
from utils.orm_io import dbIO


class DashboardHandler(SecureHandler):
    login_url = '/pyfaas/login'

    def initialize(self, *args, **kwargs):
        super().initialize(*args, **kwargs)
        self.io = dbIO(
            db_server=self.conf['address'],
            port=self.conf.get('port', 3306),
            username=self.conf.get('username'),
            password=self.conf.get('password'),
            database=self.conf['name']
        )

    @authentication_required
    def get(self):
        functions = self.io.query(Function, user_id=self.user.user_id)
        return self.render('functions.html', functions=[func.as_dict() for func in functions])