#coding:utf-8

from tornado.web import RequestHandler
import json
from util.convert import is_mobile
import logging

LOG = logging.getLogger(__name__)

class DefaultHandler(RequestHandler):
    def initialize(self, static_path, templates_path, product_prefix, **kwds):
        self.static_path = static_path
        self.templates_path = templates_path

        if product_prefix[-1] != '/':
            product_prefix += '/'
        self.prefix = product_prefix

    def get_template_path(self):
        return self.templates_path

    def get(self):
        self.redirect(self.prefix + r'school.html', permanent=True)

class RegistryViewHandler(RequestHandler):
    def initialize(self, static_path, templates_path, **kwds):
        self.static_path = static_path
        self.templates_path = templates_path

    def get_template_path(self):
        return self.templates_path

    def get(self):
        #real_ip = self.request.headers.get("x-real-ip", self.request.headers.get("x-forwarded-for", ""))

        self.render('school_input.html', user_name=self.get_secure_cookie('user_name'))