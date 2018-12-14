from handlers.login_handler import LoginHandler
from handlers.logout_handler import LogoutHandler
from handlers.register_handler import RegisterHandler
from handlers.upload_handler import UploadHandler
from handlers.dashboard_handler import DashboardHandler
from handlers.execution_handler import ExecutionHandler

def buildUrls(services_conf=None):
    url_patterns = [
        (r"/pyfaas/upload", UploadHandler, {'config': services_conf['database'], 'session': True, 'broker': services_conf['broker']}),
        (r"/pyfaas/function/(.*)", ExecutionHandler, {'config': services_conf['database'], 'broker': services_conf['broker']}),
        (r"/pyfaas/login", LoginHandler, {'config': services_conf['database'], 'session': True}),
        (r"/pyfaas/logout", LogoutHandler, {'config': services_conf['database'], 'session': True}),
        (r"/pyfaas/register", RegisterHandler, {'config': services_conf['database'], 'session': True}),
        (r"/pyfaas/functions", DashboardHandler, {'config': services_conf['database'], 'session': True})

        ]
    return url_patterns