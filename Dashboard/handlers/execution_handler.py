from middlewares.base_handler import SecureHandler
from models.functions import Function
from utils.orm_io import dbIO
from utils.rabbitmq import FaaSClient
import json


class ExecutionHandler(SecureHandler):
    login_url = 'pyfaas/login'

    def initialize(self, *args, **kwargs):
        super().initialize(*args, **kwargs)
        self.broker_conf = kwargs['broker']
        self.io = dbIO(
            db_server=self.conf['address'],
            port=self.conf.get('port', 3306),
            username=self.conf.get('username'),
            password=self.conf.get('password'),
            database=self.conf['name']
        )
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        if self.request.headers.get("Content-Type") != "application/json":
            self.set_status(415)
            self.finish()

    def post(self, function_uuid):
        if self.request.body:
            try:
                body = json.loads(self.request.body.decode("utf-8"))
            except Exception as e:
                self.set_status(415)
                self.write(json.dumps({"error": f"failed to get json body due to exception: {str(e)}"}))
                self.finish()
        else:
            body = {}
        function = self.io.query(Function, function_uuid=function_uuid)
        if not function:
            self.set_status(404)
            self.finish()
        function = function[0]
        client = FaaSClient(
            host=self.broker_conf.get('address'),
            port=self.broker_conf.get('port'),
            username=self.broker_conf.get('username'),
            password=self.broker_conf.get('password'),
            vhost=self.broker_conf.get('vhost', '/')
        )
        try:
            result = client.call_blocking_function(
                func_uuid=function.function_uuid,
                body=body
            )
        except TimeoutError as e:
            self.set_status(408)
            self.write(json.dumps({"errors": str(e)}))
            self.finish()
        self.write(json.dumps(result))
        self.set_status(200)
        self.finish()


    def options(self):
        self.set_status(200)
        self.finish()
