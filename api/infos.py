#coding:utf-8

from tornado.web import RequestHandler
import json
from util.convert import is_mobile
import logging

LOG = logging.getLogger(__name__)

class InfosHandler(RequestHandler):
    def _get_school_argument(self):
        code = self.get_argument('code', '')
        name = self.get_argument('name', '')
        cardcode = self.get_argument('cardcode', '')

    def _get_class_argument(self):
        code = self.get_argument('code', '')
        name = self.get_argument('name', '')
        grade = self.get_argument('grade', '')
        school_code = self.get_argument('school_code', '')
        school_name = self.get_argument('school_code', '')

    def _get_teacher_argument(self):
        code = self.get_argument('code', '')
        name = self.get_argument('name', '')
        school_code = self.get_argument('school_code', '')
        school_name = self.get_argument('school_name', '')
        class_code = self.get_argument('school_code', '')
        class_name = self.get_argument('class_name', '')

    def _get_student_argument(self):
        code = self.get_argument('code', '')
        name = self.get_argument('name', '')
        grade = self.get_argument('grade', '')
        school_code = self.get_argument('school_code', '')
        school_name = self.get_argument('school_name', '')
        class_code = self.get_argument('class_code', '')
        class_name = self.get_argument('class_name', '')
        relative_code = self.get_argument('relative_code', '')
        relative_name = self.get_argument('relative_name', '')

    def _get_relative_argument(self):

        code = self.get_argument('code', '')
        name = self.get_argument('name', '')
        student_code = self.get_argument('student_code', '')
        student_name = self.get_argument('student_name', '')
        school_code = self.get_argument('school_code', '')
        school_name = self.get_argument('school_name', '')
        phone = self.get_argument('phone', '')

    def _org_argument(self, registry_obj):
        if registry_obj == "school":
            return self._get_school_argument()
            pass

    def get(self, registry_obj):
        if registry_obj == "school":

            pass