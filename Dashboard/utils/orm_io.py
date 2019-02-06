#/usr/bin/python3.6

from sqlalchemy import create_engine, func, desc
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker

class dbIO(object):
    '''interface used to interact with database objects'''
    def __init__(self, db_server, username, password, database, port=3306):
        uri = f"mysql+pymysql://{username}:{password}@{db_server}:{port}/{database}"
        engine = create_engine(uri)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def query(self, cl, **kwargs):
        res = self.session.query(cl).filter_by(**kwargs).all()
        return res

    def search(self, cl, per_page, page_number, order_by, simple_filters={}, range_filters={}, desc_flag=False):
        for range_filter in range_filters:
            all_obj = self.session.query(cl).filter(getattr(cl, range_filter)>=range_filters[range_filter]['gte'], getattr(cl, range_filter)<=range_filters[range_filter]['lte'])
            print(range_filter, all_obj.all())
        if desc_flag:
            all_obj = all_obj.filter_by(**simple_filters).order_by(desc(getattr(cl, order_by))).all()
        else:    
            all_obj = all_obj.session.query(cl).filter_by(**simple_filters).order_by(getattr(cl, order_by)).all()
        no_pages = int(len(all_obj) / per_page) + (len(all_obj) % per_page > 0)
        return all_obj[((page_number-1)*per_page):page_number*per_page], no_pages

    def generatorQuery(self, cl, **kwargs):
        for res in self.session.query(cl).filter_by(**kwargs).all():
            yield res

    def add(self, objs=[]):
        for obj in objs:
            self.session.add(obj)
        self.session.commit()
        self.session.flush()

    def delete(self, objs=[]):
        for obj in objs:
            self.session.delete(obj)
        self.session.commit()
        self.session.flush()

    def update(self, obj, update_dict={}):
        for attr in update_dict:
            setattr(obj, attr, update_dict[attr])
        self.session.commit()
        self.session.flush()