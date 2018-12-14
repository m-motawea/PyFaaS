import os, sys
import base64

class FaaSPackage(object):
    def __init__(self, name, uuid, code, requirements, py_version, functions_path=None, **broker_config):
        self.name = name
        self.uuid = uuid
        self.function_queue = self.uuid
        self.code = base64.b64decode(code).decode("utf-8")
        self.requirements = base64.b64decode(requirements).decode("utf-8") + "\npika"
        self.version = py_version
        self.broker_address = broker_config.get("broker_address")
        self.broker_port = broker_config.get("broker_port")
        self.broker_username = broker_config.get("broker_username")
        self.broker_password = broker_config.get("broker_password")

        if functions_path:
            self.functions_path = functions_path
        else:
            self.functions_path = os.environ.get("FUNCTIONS_PATH")
        self.path = self.functions_path + "/" + self.name

        if not os.path.exists(self.path):
            self.init_directory()


    def init_directory(self):
        if not os.path.exists(self.functions_path):
            os.mkdir(self.functions_path)
        os.mkdir(self.path)
        os.system(f"touch {self.path}/__init__.py")
        os.system(f"touch {self.path}/consumer.py")
        os.system(f"touch {self.path}/.env")
        os.system(f"touch {self.path}/function.py")
        os.system(f"touch {self.path}/requirements.txt")


    def generate_code(self):
        os.system(f"cat worker/consumer.py > {self.path}/consumer.py")
        os.system(f'echo "{self.code}" > {self.path}/function.py')
        os.system(f'echo "{self.requirements}" > {self.path}/requirements.txt')


    def generate_env_dict(self):
        self.env_dict = {
            "BROKER_ADDRESS": self.broker_address,
            "BROKER_PORT": self.broker_port,
            "BROKER_USERNAME": self.broker_username,
            "BROKER_PASSWORD": self.broker_password,
            "FUNCTION_NAME": self.name,
            "FUNCTION_QUEUE": self.function_queue
        }