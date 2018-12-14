#!/usr/bin/python3.6
from models import base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
import datetime
from models.auth import User

class Function(base):
    __tablename__ = 'functions'

    function_id = Column(Integer, primary_key=True)
    function_uuid = Column(String(255), nullable=False, unique=True)
    function_name = Column(String(30), nullable=False)
    created = Column(DateTime, default=datetime.datetime.now())
    is_available = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey(f'{User.__tablename__}.user_id'), nullable=True)

    def as_dict(self):
        return {
            'id': self.function_id,
            'uuid': self.function_uuid,
            'name': self.function_name,
            'created': str(self.created),
            'is_available': self.is_available
        }