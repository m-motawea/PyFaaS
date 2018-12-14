#!/usr/bin/python3.6
import sys, os

PROJECT_ROOT = os.path.abspath(os.path.join(__file__, os.pardir))
sys.path.insert(0, PROJECT_ROOT)

import tornado.httpserver
import tornado.ioloop
import tornado.autoreload
from utils.config_parser import getConfig
from app import create_application


conf = getConfig('config.json')

def create_server():
    app = create_application(conf)
    try:
        tornado.autoreload.start(conf['autoreload'])
        tornado.autoreload.watch('config.json')
    except Exception as e:
        print(str(e))
    
    #creating web server
    if conf['certfile'] and conf['keyfile']:
        http_server = tornado.httpserver.HTTPServer(app, ssl_options={"certfile": conf['certfile'], "keyfile": conf['keyfile']})
    else:
        print('starting as http')
        http_server = tornado.httpserver.HTTPServer(app)
    
    try:
        http_server.listen(conf['port'])
    except Exception as e:
        print(str(e))
        exit()

    return http_server



def start(http_server):
    try:
        try:
            http_server.start(conf['processes'])
        except Exception as e:
            print(str(e))
            exit()
        ioloop = tornado.ioloop
        loop = ioloop.IOLoop.current()
        loop.start()
    except KeyboardInterrupt:
        if conf['processes'] != 1:
            os.system('pkill -9 server.py')
        else:
            exit()

if __name__ == '__main__':
    http_server = create_server()
    start(http_server)