#coding:utf-8

from tornado.web import RequestHandler
import json
from util.convert import is_mobile
import logging

LOG = logging.getLogger(__name__)

class RegistryViewHandler(RequestHandler):
    def get(self, registry_obj):
        if registry_obj == "school":
            self.render('school_input.html', user_name=self.get_secure_cookie('user_name'))
        pass