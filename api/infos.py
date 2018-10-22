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
        id = self.get_argument('id', '')
        name = self.get_argument('name', '')
        cardcode = self.get_argument('cardcode', '')
        return {
            "id": id,
            "name": name,
            "cardcode": cardcode
        }

    def _get_class_argument(self):
        id = self.get_argument('id', '')
        name = self.get_argument('name', '')
        grade = self.get_argument('grade', '')
        school_id = self.get_argument('school_id', '')
        school_name = self.get_argument('school_name', '')
        return {
            "id": id,
            "name": name,
            "grade": grade,
            "school_id": school_id,
            "school_name": school_name
        }

    def _get_teacher_argument(self):
        id = self.get_argument('id', '')
        name = self.get_argument('name', '')
        school_id = self.get_argument('school_id', '')
        school_name = self.get_argument('school_name', '')
        class_id = self.get_argument('school_id', '')
        class_name = self.get_argument('class_name', '')
        phone = self.get_argument('phone', '')
        return {
            "id": id,
            "name": name,
            "school_id": school_id,
            "school_name": school_name,
            "class_id": class_id,
            "class_name": class_name,
            "phone": phone
        }

    def _get_student_argument(self):
        id = self.get_argument('id', '')
        name = self.get_argument('name', '')
        grade = self.get_argument('grade', '')
        school_id = self.get_argument('school_id', '')
        school_name = self.get_argument('school_name', '')
        class_id = self.get_argument('class_id', '')
        class_name = self.get_argument('class_name', '')
        relative_id = self.get_argument('relative_id', '')
        relative_name = self.get_argument('relative_name', '')
        return {
            "id": id,
            "name": name,
            "grade": grade,
            "school_id": school_id,
            "school_name": school_name,
            "class_id": class_id,
            "class_name": class_name,
            "relative_id": relative_id,
            "relative_name": relative_name
        }


    def _get_relative_argument(self):
        id = self.get_argument('id', '')
        name = self.get_argument('name', '')
        student_id = self.get_argument('student_id', '')
        student_name = self.get_argument('student_name', '')
        school_id = self.get_argument('school_id', '')
        school_name = self.get_argument('school_name', '')
        phone = self.get_argument('phone', '')
        return {
            "id": id,
            "name": name,
            "student_id": student_id,
            "student_name": student_name,
            "school_id": school_id,
            "school_name": school_name,
            "phone": phone
        }
