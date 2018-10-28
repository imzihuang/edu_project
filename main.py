#!/usr/bin/python
# -*- coding: utf-8 -*-

from tornado import httpserver
from tornado.web import URLSpec, StaticFileHandler, Application
from tornado.options import define, options
from tornado.ioloop import IOLoop
from setproctitle import setproctitle
from api import api_handlers
from views import views_handlers
import settings
import logging

define("port", default=9090, help="run on the given port", type=int)
print options.port
setproctitle('edu:server')

if settings.default_settings.get("log_info", ""):
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s  %(filename)s : %(levelname)s  %(message)s',
                        filename=settings.default_settings.get("log_info", ""),
                        datefmt='%Y-%m-%d %A %H:%M:%S', )

if settings.default_settings.get("log_error", ""):
    logging.basicConfig(level=logging.ERROR,
                        format='%(asctime)s  %(filename)s : %(levelname)s  %(message)s',
                        filename=settings.default_settings.get("log_error", ""),
                        datefmt='%Y-%m-%d %A %H:%M:%S', )


class My_Application(Application):
    def __init__(self, handlers=None, default_host="", **settings):
        super(My_Application, self).__init__(handlers, default_host, **settings)

def make_app():
    settings = {
        'cookie_secret': "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
    }
    return My_Application(api_handlers + views_handlers, **settings)

if __name__ == "__main__":
    app = make_app()
    server = httpserver.HTTPServer(app, xheaders=True)
    server.bind(options.port)
    server.start(0)
    IOLoop.instance().start()
