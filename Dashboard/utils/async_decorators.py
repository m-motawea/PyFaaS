from concurrent.futures import ThreadPoolExecutor
from functools import partial, wraps
import tornado

EXECUTOR = ThreadPoolExecutor(max_workers=4)


def unblock(f):

    @tornado.web.gen.coroutine
    @wraps(f)
    def wrapper(*args, **kwargs):
        self = args[0]

        def callback(future):
            self.write(future.result())
            self.finish()

        EXECUTOR.submit(
            partial(f, *args, **kwargs)
        ).add_done_callback(
            lambda future: tornado.ioloop.IOLoop.instance().add_callback(
                partial(callback, future)))

    return wrapper
