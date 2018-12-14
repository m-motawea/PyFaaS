import tornado.web
from urls import buildUrls


def create_application(conf):
    urls = buildUrls(conf)
    app = tornado.web.Application(
        handlers=urls,
        template_path="templates",
        static_path="static",
        debug=True,
        cookie_secret=conf.get('cookie_secret')
        )
    return app