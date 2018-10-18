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

define("port", default=8080, help="run on the given port", type=int)
setproctitle('edu:server')

if settings.default_settings.get("log_path", ""):
    logging.basicConfig(filename=settings.default_settings.get("log_path", ""))


class My_Application(Application):
    def __init__(self, handlers=None, default_host="", **settings):
        super(My_Application, self).__init__(handlers, default_host, **settings)

def make_app():
    settings = {
        'cookie_secret': "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
    }
    return My_Application(api_handlers + views_handlers, **settings)

if __name__ == "__main__":
    options.logging = 'info'
    app = make_app()
    server = httpserver.HTTPServer(app, xheaders=True)
    server.bind(options.port)
    server.start(0)
    IOLoop.instance().start()

    #app.listen(options.port)
    #tornado.ioloop.IOLoop.current().start()
