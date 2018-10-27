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
from logic.relation import RelationLogic

LOG = logging.getLogger(__name__)

class UpdateHandler(RequestHandler):
    def post(self, update_obj):
        try:
            _id = ""
            _value = {}
            _op = Logic()
            if update_obj == "school":
                _id, _value = self._get_school_argument()
                _op = SchoolLogic()

            if update_obj == "class":
                _id, _value = self._get_class_argument()
                _op = ClassLogic()

            if update_obj == "teacher":
                _id, _value = self._get_teacher_argument()
                _op = TeacherLogic()

            if update_obj == "student":
                _id, _value = self._get_student_argument()
                _op = StudentLogic()

            if update_obj == "relative":
                _id, _value = self._get_relative_argument()
                _op = RelativeLogic()

            if update_obj == "relation":
                _id, _value = self._get_relation_argument()
                _op = RelationLogic()

            if not _value or not _id:
                self.finish(json.dumps({'state': 9, 'message': 'params %s is None' % update_obj}))
            _ = _op.update(_id, **_value)
            if not _:
                self.finish(json.dumps({'state': 0, 'message': 'update info success.'}))
            else:
                self.finish(json.dumps({'state': 10, 'message': 'action %s error' % update_obj}))
        except Exception as ex:
            LOG.error("Input %s error:%s" % (update_obj, ex))
            self.finish(json.dumps({'state': 10, 'message': 'update action error'}))


    def _get_school_argument(self):
        id = self.get_argument('id', '')
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
        return id, result

    def _get_class_argument(self):
        id = self.get_argument('id', '')
        name = self.get_argument('name', '')
        grade = self.get_argument('grade', '')
        cardcode = self.get_argument('cardcode', '')
        school_id = self.get_argument('school_id', '')
        student_number = int(self.get_argument('study_number', 0))
        result = {}
        if name:
            result.update({"name", name})
        if grade:
            result.update({"grade": grade})
        if cardcode:
            result.update({"cardcode": cardcode})
        if school_id:
            result.update({"school_id": school_id})
        if student_number:
            result.update({"student_number": student_number})
        return id, result

    def _get_teacher_argument(self):
        id = self.get_argument('id', '')
        name = self.get_argument('name', '')
        sex = int(self.get_argument('sex', 0))
        age = int(self.get_argument('age', 0))
        school_id = self.get_argument('school_id', '')
        class_id = self.get_argument('class_id', '')
        phone = self.get_argument('phone', '')
        result = {}
        if name:
            result.update({"name", name})
        if sex:
            result.update({"sex": sex})
        if age:
            result.update({"age": age})
        if school_id:
            result.update({"school_id": school_id})
        if class_id:
            result.update({"class_id": class_id})
        if phone:
            result.update({"phone": phone})
        return id, result


    def _get_student_argument(self):
        id = self._get_argument('id', '')
        name = self.get_argument('name', '')
        sex = int(self.get_argument('sex', 0))
        age = int(self.get_argument('age', 0))
        class_id = self.get_argument('class_id', '')
        school_id = self.get_argument('school_id', '')
        status = self.get_argument('status', 'apply')
        relation_number = int(self.get_argument('relation_number', 3))
        result = {}
        if name:
            result.update({"name", name})
        if sex:
            result.update({"sex": sex})
        if age:
            result.update({"age": age})
        if school_id:
            result.update({"school_id": school_id})
        if class_id:
            result.update({"class_id": class_id})
        if status:
            result.update({"status": status})
        if relation_number:
            result.update({"relation_number": relation_number})
        return id, result

    def _get_relative_argument(self):
        id = self._get_argument('id', '')
        name = self.get_argument('name', '')
        sex = int(self.get_argument('sex', 0))
        age = int(self.get_argument('age', 0))
        phone = self.get_argument('phone', '')
        result = {}
        if name:
            result.update({"name", name})
        if sex:
            result.update({"sex": sex})
        if age:
            result.update({"age": age})
        if phone:
            result.update({"phone": phone})
        return id, result

    def _get_relation_argument(self):
        id = self._get_argument('id', '')
        relation = self.get_argument('relation', '')
        student_id = self.get_argument('student_id', '')
        relative_id = self.get_argument('relative_id', '')
        result = {
            "relation": relation,
            "student_id": student_id,
            "relative_id": relative_id
        }
        return id, result

