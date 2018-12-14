#!/usr/bin/python3.6
from models import base
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy import MetaData
import datetime
import random
import hashlib
import time
from passlib.context import CryptContext

pwd_context = CryptContext(default="django_pbkdf2_sha256", schemes=["django_pbkdf2_sha256"])
SECRET_KEY='mysecretkey'

def generate_session_id():
    length = 12
    allowed_chars=[*list('abcdefghijklmnopqrstuvwxyz'), *list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')]
    random.seed(
            hashlib.sha256(
                ("%s%s%s" % (
                    random.getstate(),
                    time.time(),
                    SECRET_KEY
                )).encode('utf-8')
            ).digest()
        )
    return ''.join(random.choice(allowed_chars) for i in range(length))


class User(base):
    __tablename__ = 'auth_user'

    user_id = Column(Integer, primary_key=True)
    user_name = Column(String(50), nullable=False)
    user_password = Column(String(255), nullable=False)
    user_email = Column(String(60), nullable=False, unique=True)

    def hash_password(self):
        self.user_password = pwd_context.hash(self.user_password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.user_password)


class Session(base):
    __tablename__ = 'auth_session'

    _id = Column(Integer, primary_key=True)
    session_id = Column(String(255), nullable=False, unique=True, default=generate_session_id)
    expires = Column(DateTime, default=datetime.datetime.now()+datetime.timedelta(days=3))
    user_id = Column(Integer, ForeignKey(f'{User.__tablename__}.user_id', ondelete='CASCADE', onupdate='CASCADE'))

    def is_expired(self):
        return self.expires < datetime.datetime.now()