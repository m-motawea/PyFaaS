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
        """parameters:
            - cl > class of sqlalchemy orm
            returns a list of objects
            example:
                io = dbIO('127.0.0.1')
                areas = io.query(OttAction, item_name='item-01')"""
        res = self.session.query(cl).filter_by(**kwargs).all()
        return res

    def search(self, cl, per_page, page_number, order_by, simple_filters={}, range_filters={}, desc_flag=False):
        """parameters:
            - cl > class of sqlalchemy orm
            - per_page > number of how many items per page (int)
            - page_number > number of current page (int)
            - order_by > attribute name to order the return list by (str)
            - simple_filters > a dictionary contatining attribute names and their values to search by (dict)
            - range_filters > a dictionary containing attribute names as keys and dict values containing 'lte' and 'gte' keys (dict of dicts)
        returns a list of objects and number of pages
        example:
            result, no_pages = io.search(
            OttAction,
            per_page=10,
            page_number=2,
            order_by='date',
            simple_filters={'user_id': 1},
            range_filters={'date': {'gte': str(datetime.datetime.now() + datetime.time_delta(-30)), 'lte': str(datetime.datetime.now())}},
            desc_flag=True
        )
        """
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
        """parameters:
            - cl > class of sqlalchemy orm
            retruns a generator
            example:
                io = dbIO('127.0.0.1')
                g = io.generatorQuery(OttAction)
                a = next(g)
        """
        for res in self.session.query(cl).filter_by(**kwargs).all():
            yield res

    def add(self, objs=[]):
        """parameters:
            - objs > a list of the objects to be added
            no return
            example:
                a1 = OttAction()
                a2 = OttAction
                io = dbIO('127.0.0.1')
                io.add([a1, a2])
        """
        for obj in objs:
            self.session.add(obj)
        self.session.commit()
        self.session.flush()

    def delete(self, objs=[]):
        """parameters:
            - objs > a list of the objects to be deleted
            no return
        """
        for obj in objs:
            self.session.delete(obj)
        self.session.commit()
        self.session.flush()

    def update(self, obj, update_dict={}):
        """parameters:
            - obj > the object to be updated
            - update_dict > dictionary containing pairs of attribute name(str) and new value
            returns modified object
            example:
                io = dbIO('127.0.0.1')
                actions = io.query(OttAction)
                a = io.update(actions[-1], {'item_name': 'New_Name'})
        """
        q = self.session.query(type(obj)).all()
        for o in q:
            if obj == o:
                for attr in update_dict:
                    setattr(o, attr, update_dict[attr])
                self.session.commit()
                break
        self.session.flush()

    def __del__(self):
        self.session.close()