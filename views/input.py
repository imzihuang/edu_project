#coding:utf-8

from tornado.web import RequestHandler
import json
from util.convert import is_mobile
import logging

LOG = logging.getLogger(__name__)

class DefaultHandler(RequestHandler):
    def initialize(self, static_path, templates_path, view_prefix, **kwargs):
        self.static_path = static_path
        self.templates_path = templates_path

        if view_prefix[-1] != '/':
            view_prefix += '/'
        self.prefix = view_prefix

    def get_template_path(self):
        return self.templates_path

    def get(self):
        self.redirect(self.prefix + r'login.html', permanent=True)

class LoginViewHandler(RequestHandler):
    def initialize(self, static_path, templates_path, **kwargs):
        self.static_path = static_path
        self.templates_path = templates_path

    def get_template_path(self):
        return self.templates_path

    def get(self):
        LOG.info("-----------------login-----------")
        self.render("login.html")

class IndextHandler(RequestHandler):
    def initialize(self, static_path, templates_path, view_prefix, **kwargs):
        self.static_path = static_path
        self.templates_path = templates_path

        if view_prefix[-1] != '/':
            view_prefix += '/'
            self.prefix = view_prefix

    def get_template_path(self):
        return self.templates_path

    def get(self):
        LOG.info("-----------------index-----------:%s"%self.get_secure_cookie('user_name'))
        if not self.get_secure_cookie('user_name'):
            #self.redirect(self.prefix + r'login.html', permanent=True)
            self.redirect(self.prefix + r'login.html')
            return
        self.render("index.html")


html_path = (
    "grade",
    "class",
    "teacher",
    "student",
    "relative",
    "studentHistory",
    "teacherHistory",
    "school",
    "studentAttendance",
    "teacherAttendance",
    "loginPhone",
    "commonPerson",
    "studentAttendance",
    "forgetPassword")


class ManageViewHandler(RequestHandler):
    def initialize(self, static_path, templates_path, **kwds):
        self.static_path = static_path
        self.templates_path = templates_path

    def get_template_path(self):
        return self.templates_path

    def get(self, manage_obj):
        #real_ip = self.request.headers.get("x-real-ip", self.request.headers.get("x-forwarded-for", ""))
        if manage_obj not in html_path:
            self.redirect(r'login.html', permanent=True)
            return

        self.render(manage_obj + r'.html', user_name=self.get_secure_cookie('user_name'))