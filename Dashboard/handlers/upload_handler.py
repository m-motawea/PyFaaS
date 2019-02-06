import tornado.web
from utils.rabbitmq import FaaSClient
from utils.orm_io import dbIO
from middlewares.base_handler import SecureHandler
from middlewares.decorators import authentication_required
from models.functions import Function
from utils.async_decorators import unblock

class UploadHandler(SecureHandler):
    login_url = '/pyfaas/login'
    
    def initialize(self, *args, **kwargs):
        super().initialize(*args, **kwargs)
        self.broker_conf = kwargs['broker']

    @authentication_required
    def get(self):
        self.render('upload_form.html')

    @authentication_required
    def post(self):
        code = self.request.files['code'][0]['body']
        if self.request.files.get('requirements'):
            requirements = self.request.files['requirements'][0]['body']
        else:
            requirements = ""
        name = self.get_argument('function')
        version = self.get_argument("version")
        client = FaaSClient(
            host=self.broker_conf.get('address'),
            port=self.broker_conf.get('port'),
            username=self.broker_conf.get('username'),
            password=self.broker_conf.get('password'),
            vhost=self.broker_conf.get('vhost', '/')
        )
        function_uuid = client.create_function(name, code, requirements, version)
        io = dbIO(
                db_server=self.conf['address'],
                port=self.conf.get('port', 3306),
                username=self.conf.get('username'),
                password=self.conf.get('password'),
                database=self.conf['name']
            )
        new_func = Function(
            function_uuid=function_uuid,
            function_name=name,
            user_id=self.user.user_id
        )
        io.add([new_func])
        return self.redirect('/pyfaas/functions')