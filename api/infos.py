#coding:utf-8

from tornado.web import RequestHandler
import json
from util.convert import is_mobile
import logging

from logic import Logic
from logic.school import SchoolLogic
from logic.classlogic import ClassLogic
from logic.teacher import TeacherLogic
from logic.student import StudentLogic
from logic.relative import RelativeLogic

LOG = logging.getLogger(__name__)

class InfosHandler(RequestHandler):
    def get(self, infos_obj):
        limit = int(self.get_argument('limit', 100))
        offset = int(self.get_argument('offset', 1))
        try:
            _op = Logic()
            _value = dict()
            if infos_obj == "school":
                _value = self._get_school_argument()
                _op = SchoolLogic()

            if infos_obj == "class":
                _value = self._get_class_argument()
                _op = ClassLogic()

            if infos_obj == "teacher":
                _value = self._get_teacher_argument()
                _op = TeacherLogic()

            if infos_obj == "student":
                _value = self._get_student_argument()
                _op = StudentLogic()

            if infos_obj == "relative":
                _value = self._get_relative_argument()
                _op = RelativeLogic()

            _ = _op.infos(limit=limit, offset=offset, **_value)
            if _:
                self.finish(json.dumps(_))
            else:
                self.finish(json.dumps({'state': 10, 'message': 'action %s error'%infos_obj}))
        except Exception as ex:
            LOG.error("query %s error:%s"%(infos_obj, ex))
            self.finish(json.dumps({"count": 0, "state":1, "message":"error", "data":[]}))


    def _get_school_argument(self):
        code = self.get_argument('code', '')
        name = self.get_argument('name', '')
        cardcode = self.get_argument('cardcode', '')
        return {
            "code": code,
            "name": name,
            "cardcode": cardcode
        }

    def _get_class_argument(self):
        code = self.get_argument('code', '')
        name = self.get_argument('name', '')
        grade = self.get_argument('grade', '')
        school_code = self.get_argument('school_code', '')
        school_name = self.get_argument('school_code', '')
        return {
            "code": code,
            "name": name,
            "grade": grade,
            "school_code": school_code,
            "school_name": school_name
        }

    def _get_teacher_argument(self):
        code = self.get_argument('code', '')
        name = self.get_argument('name', '')
        school_code = self.get_argument('school_code', '')
        school_name = self.get_argument('school_name', '')
        class_code = self.get_argument('school_code', '')
        class_name = self.get_argument('class_name', '')
        phone = self.get_argument('phone', '')
        return {
            "code": code,
            "name": name,
            "school_code": school_code,
            "school_name": school_name,
            "class_code": class_code,
            "class_name": class_name,
            "phone": phone
        }

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
        return {
            "code": code,
            "name": name,
            "grade": grade,
            "school_code": school_code,
            "school_name": school_name,
            "class_code": class_code,
            "class_name": class_name,
            "relative_code": relative_code,
            "relative_name": relative_name
        }


    def _get_relative_argument(self):
        code = self.get_argument('code', '')
        name = self.get_argument('name', '')
        student_code = self.get_argument('student_code', '')
        student_name = self.get_argument('student_name', '')
        school_code = self.get_argument('school_code', '')
        school_name = self.get_argument('school_name', '')
        phone = self.get_argument('phone', '')
        return {
            "code": code,
            "name": name,
            "student_code": student_code,
            "student_name": student_name,
            "school_code": school_code,
            "school_name": school_name,
            "phone": phone
        }
