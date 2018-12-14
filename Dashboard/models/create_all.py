import sys
import os
PROJECT_ROOT = os.path.abspath(os.path.join(__file__, os.pardir))[:-7]
print(PROJECT_ROOT)
sys.path.insert(0, PROJECT_ROOT)

from sqlalchemy import create_engine
from models import base


def create_tables(uri, tables=[]):
    engine = create_engine(uri)
    if not tables:
        base.metadata.create_all(engine)
    else:
        base.metadata.create_all(engine, tables=tables)


if __name__ == '__main__':
    from models.functions import Function
    from models.auth import User, Session
    uri = 'mysql+mysqldb://root:root@mysql/pyfaas_dashboard'
    create_tables(uri, [User.__table__, Session.__table__, Function.__table__])