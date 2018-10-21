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

class UpdateHandler(RequestHandler):
    def post(self, update_obj):
        _code = ""
        _value = {}
        _op = Logic()
        if update_obj == "school":
            _code, _value = self._get_school_argument()
            _op = SchoolLogic()

        if update_obj == "class":
            _code, _value = self._get_class_argument()
            _op = ClassLogic()

        if update_obj == "teacher":
            _code, _value = self._get_teacher_argument()
            _op = TeacherLogic()

        if update_obj == "student":
            _code, _value = self._get_student_argument()
            _op = StudentLogic()

        if update_obj == "relative":
            _code, _value = self._get_relative_argument()
            _op = RelativeLogic()

        if not _value or not _code:
            self.finish(json.dumps({'state': 9, 'message': 'params %s is None' % update_obj}))
        _ = _op.update(_code, **_value)
        if not _:
            self.finish(json.dumps({'state': 0, 'message': 'update info success.'}))
        else:
            self.finish(json.dumps({'state': 10, 'message': 'action %s error' % update_obj}))
        pass

    def _get_school_argument(self):
        code = self.get_argument('code', '')
        name = self.get_argument('name', '')
        cardcode = self.get_argument('cardcode', '')
        describe = self.get_argument('describe', '')
        result = {}
        if name:
            result.update({"name", name})
        if cardcode:
            result.update({"cardcode": cardcode})
        if describe:
            result.update({"describe": describe})
        return code, result

    def _get_class_argument(self):
        code = self.get_argument('code', '')
        name = self.get_argument('name', '')
        grade = self.get_argument('grade', '')
        school_code = self.get_argument('school_code', '')
        student_number = int(self.get_argument('study_number', 0))
        result = {}
        if name:
            result.update({"name", name})
        if grade:
            result.update({"grade": grade})
        if school_code:
            result.update({"school_code": school_code})
        if student_number:
            result.update({"student_number": student_number})
        return code, result

    def _get_teacher_argument(self):
        code = self.get_argument('code', '')
        name = self.get_argument('name', '')
        sex = int(self.get_argument('sex', 0))
        age = int(self.get_argument('age', 0))
        school_code = self.get_argument('school_code', '')
        class_code = self.get_argument('school_code', '')
        phone = self.get_argument('phone', '')
        result = {}
        if name:
            result.update({"name", name})
        if sex:
            result.update({"sex": sex})
        if age:
            result.update({"age": age})
        if school_code:
            result.update({"school_code": school_code})
        if class_code:
            result.update({"class_code": class_code})
        if phone:
            result.update({"phone": phone})
        return code, result


    def _get_student_argument(self):
        code = self._get_argument('code', '')
        name = self.get_argument('name', '')
        sex = int(self.get_argument('sex', 0))
        age = int(self.get_argument('age', 0))
        grade = self.get_argument('grade', '')
        class_code = self.get_argument('class_code', '')
        school_code = self.get_argument('school_code', '')
        status = self.get_argument('status', 'apply')
        relation_number = int(self.get_argument('school_code', 3))
        result = {}
        if name:
            result.update({"name", name})
        if sex:
            result.update({"sex": sex})
        if age:
            result.update({"age": age})
        if grade:
            result.update({"grade": grade})
        if school_code:
            result.update({"school_code": school_code})
        if class_code:
            result.update({"class_code": class_code})
        if status:
            result.update({"status": status})
        if relation_number:
            result.update({"relation_number": relation_number})
        return code, result

    def _get_relative_argument(self):
        code = self._get_argument('code', '')
        name = self.get_argument('name', '')
        sex = int(self.get_argument('sex', 0))
        age = int(self.get_argument('age', 0))
        student_code = self.get_argument('student_code', '')
        relation = self.get_argument('relation', '')
        phone = self.get_argument('phone', '')
        result = {}
        if name:
            result.update({"name", name})
        if sex:
            result.update({"sex": sex})
        if age:
            result.update({"age": age})
        if student_code:
            result.update({"class_code": student_code})
        if relation:
            result.update({"relation": relation})
        if phone:
            result.update({"phone": phone})
        return code, result

