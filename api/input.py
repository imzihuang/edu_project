#coding:utf-8

from tornado.web import RequestHandler
import json
from util.exception import ParamExist
import logging

from util import convert
from logic import Logic
from logic.school import SchoolLogic
from logic.gradelogic import GradeLogic
from logic.classlogic import ClassLogic
from logic.teacher import TeacherLogic
from logic.student import StudentLogic
from logic.relative import RelativeLogic
from logic.relation import RelationLogic
from logic.teacher_history import Teacher_HistoryLogic
from logic.student_history import Student_HistoryLogic

LOG = logging.getLogger(__name__)

class RegistryHandler(RequestHandler):
    def post(self, registry_obj):
        try:
            _op = Logic()
            _infos = dict()
            if registry_obj == "school":
                _infos = self._get_school_argument()
                _op = SchoolLogic()

            if registry_obj == "grade":
                _infos = self._get_grade_argument()
                _op = GradeLogic()

            if registry_obj == "class":
                _infos = self._get_class_argument()
                _op = ClassLogic()

            if registry_obj == "teacher":
                _infos = self._get_teacher_argument()
                _op = TeacherLogic()
            if registry_obj == "teacher_history":
                _infos = self._get_teacher_history_argument()
                _op = Teacher_HistoryLogic()

            if registry_obj == "student":
                _infos = self._get_student_argument()
                _op = StudentLogic()
            if registry_obj == "student_history":
                _infos = self._get_student_history_argument()
                _op = Student_HistoryLogic()

            if registry_obj == "relative":
                _infos = self._get_relative_argument()
                _op = RelativeLogic()

            if registry_obj == "relation":
                _infos = self._get_relation_argument()
                _op = RelationLogic()

            _ = _op.input(**_infos)
            if _:
                self.finish(json.dumps({'state': 0, 'message': 'input info success.'}))
            else:
                self.finish(json.dumps({'state': 10, 'message': 'action %s error'%registry_obj}))
        except ParamExist as ex:
            LOG.error("Input %s param error:%s" % (registry_obj, ex))
            self.finish(json.dumps({'state': 1, 'message': 'params exit'}))
        except Exception as ex:
            LOG.error("Input %s error:%s"%(registry_obj, ex))
            self.finish(json.dumps({'state': 2, 'message': 'input error'}))

    def _get_school_argument(self):
        name = convert.bs2utf8(self.get_argument('name', ''))
        cardcode = convert.bs2utf8(self.get_argument('cardcode', ''))
        describe = convert.bs2utf8(self.get_argument('describe', ''))
        return {
            "name": name,
            "cardcode": cardcode,
            "describe": describe
        }

    def _get_grade_argument(self):
        name = convert.bs2utf8(self.get_argument('name', ''))
        school_id = convert.bs2utf8(self.get_argument('school_id', ''))
        return {
            "name": name,
            "school_id": school_id,
        }

    def _get_class_argument(self):
        name = convert.bs2utf8(self.get_argument('name', ''))
        cardcode = convert.bs2utf8(self.get_argument('cardcode', ''))
        grade_id = convert.bs2utf8(self.get_argument('grade_id', ''))
        student_number = int(self.get_argument('study_number', 0))
        return {
            "name": name,
            "cardcode": cardcode,
            "grade_id": grade_id,
            "student_number": student_number
        }

    def _get_teacher_argument(self):
        name = convert.bs2utf8(self.get_argument('name', ''))
        sex = int(self.get_argument('sex', 0))
        birthday = convert.bs2utf8(self.get_argument('birthday', ''))
        class_id = convert.bs2utf8(self.get_argument('class_id', ''))
        phone = convert.bs2utf8(self.get_argument('phone', ''))
        position = int(self.get_argument('position', 0))
        describe = convert.bs2utf8(self._get_class_argument('describe', ''))
        return {
            "name": name,
            "sex": sex,
            "birthday": birthday,
            "class_id": class_id,
            "phone": phone,
            "position": position,
            "describe": describe,
        }

    def _get_teacher_history_argument(self):
        teacher_id = convert.bs2utf8(self.get_argument('teacher_id', ''))
        status = convert.bs2utf8(self.get_argument('status', ''))
        describe = convert.bs2utf8(self.get_argument('describe', ''))
        return {
            "teacher_id": teacher_id,
            "status": status,
            "describe": describe
        }

    def _get_student_argument(self):
        name = convert.bs2utf8(self.get_argument('name', ''))
        sex = int(self.get_argument('sex', 0))
        birthday = convert.bs2utf8(self.get_argument('birthday', ''))
        class_id = convert.bs2utf8(self.get_argument('class_id', ''))
        status = convert.bs2utf8(self.get_argument('status', 'apply'))
        relation_number = int(self.get_argument('relation_number', 3))
        describe = convert.bs2utf8(self._get_class_argument('describe', ''))
        return {
            "name": name,
            "sex": sex,
            "birthday": birthday,
            "class_id": class_id,
            "status": status,
            "relation_number": relation_number,
            "describe": describe,
        }

    def _get_student_history_argument(self):
        student_id = convert.bs2utf8(self.get_argument('student_id', ''))
        status = convert.bs2utf8(self.get_argument('status', ''))
        describe = convert.bs2utf8(self.get_argument('describe', ''))
        return {
            "student_id": student_id,
            "status": status,
            "describe": describe
        }

    def _get_relative_argument(self):
        name = convert.bs2utf8(self.get_argument('name', ''))
        sex = int(self.get_argument('sex', 0))
        birthday = convert.bs2utf8(self.get_argument('birthday', 0))
        phone = convert.bs2utf8(self.get_argument('phone', ''))
        describe = convert.bs2utf8(self._get_class_argument('describe', ''))
        return {
            "name": name,
            "sex": sex,
            "birthday": birthday,
            "phone": phone,
            "describe": describe,
        }

    def _get_relation_argument(self):
        relation = convert.bs2utf8(self.get_argument('relation', ''))
        student_id = convert.bs2utf8(self.get_argument('student_id', ''))
        relative_id = convert.bs2utf8(self.get_argument('relative_id', ''))
        return {
            "relation": relation,
            "student_id": student_id,
            "relative_id": relative_id
        }