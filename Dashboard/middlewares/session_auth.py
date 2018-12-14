from models.auth import User, Session
from utils.orm_io import dbIO

class SessionMiddleware():
    def __init__(self, request_handler, database_conf):
        self.conf = database_conf
        self.request_handler = request_handler
        self.io = dbIO(
                db_server=self.conf['address'],
                port=self.conf.get('port', 3306),
                username=self.conf.get('username'),
                password=self.conf.get('password'),
                database=self.conf['name']
            )

    def validate(self):
        session_id = self.request_handler.get_secure_cookie('session_id')
        if not session_id:
            return False
        else:
            session = self.io.query(Session, session_id=session_id)
            if len(session) > 0:
                session = session[0]
            else:
                session = None
            if not session:
                return False
            else:
                if session.is_expired():
                    return False
            self.request_handler.user = self.io.query(User, user_id=session.user_id)[0]
            return True

    def login(self, user):
        old_session = self.io.query(Session, user_id=user.user_id)
        if len(old_session) > 0:
            self.io.delete([old_session[0]])
        new_session = Session(
            user_id=user.user_id
        )
        self.io.add([new_session])
        if self.request_handler.get_argument('remember_me', None) :
            self.request_handler.set_secure_cookie('session_id', new_session.session_id, expires_days=None)
        else:
            self.request_handler.set_secure_cookie('session_id', new_session.session_id, expires_days=30)


    def logout(self):
        current_session = self.io.query(Session, user_id=self.request_handler.user.user_id)[0]
        if not current_session:
            return
        self.io.delete([current_session])
        self.request_handler.clear_cookie('session_id')

    def check_user(self, email, password):
        user = self.io.query(User, user_email=email)
        if len(user) > 0:
            user = user[0]
        else:
            user = None
        if not user:
            return None
        if not user.verify_password(password):
            return None
        return user

    def create_user(self, email, username, password):
        user = User(
            user_name=username,
            user_password=password,
            user_email=email
        )
        user.hash_password()
        self.io.add([user])
        session = Session(
            user_id=user.user_id
        )
        self.io.add([session])
        self.request_handler.set_secure_cookie('session_id', session.session_id, expires_days=30)