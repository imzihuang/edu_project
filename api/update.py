#coding:utf-8

from tornado.web import RequestHandler
import json
from util import convert
import logging

from util.exception import ParamExist, NotFound
from api.base_auth import auth_api_login
from logic import Logic
from logic.school import SchoolLogic
from logic.gradelogic import GradeLogic
from logic.classlogic import ClassLogic
from logic.teacher import TeacherLogic
from logic.student import StudentLogic
from logic.relative import RelativeLogic
from logic.relation import RelationLogic
from logic.userlogic import UserLogic

LOG = logging.getLogger(__name__)

class UpdateHandler(RequestHandler):
    @auth_api_login
    def post(self, update_obj):
        try:
            _id = ""
            _value = {}
            _op = Logic()
            if update_obj == "school":
                _id, _value = self._get_school_argument()
                _op = SchoolLogic()

            if update_obj == "grade":
                _id, _value = self._get_grade_argument()
                _op = GradeLogic()

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

            if update_obj == "user":
                _id, _value = self._get_user_argument()
                _op = UserLogic()

            if not _value or not _id:
                LOG.error("update info, %s params is None: %s, %r" % (update_obj, _id, _value))
                self.finish(json.dumps({'state': 1, 'message': 'params %s is None' % update_obj}))
                return
            _ = _op.update(_id, **_value)
            self.finish(json.dumps({'state': 0, 'message': 'update info success.'}))
        except NotFound as ex:
            LOG.error("Update %s param not data:%s" % (update_obj, ex))
            self.finish(json.dumps({'state': 2, 'message': 'param not data'}))
        except ParamExist as ex:
            LOG.error("Update %s param exit:%s" % (update_obj, ex))
            self.finish(json.dumps({'state': 5, 'message': 'param exit'}))
        except Exception as ex:
            LOG.error("Update %s error:%s" % (update_obj, ex))
            self.finish(json.dumps({'state': 3, 'message': 'update action error'}))


    def _get_school_argument(self):
        id = convert.bs2utf8(self.get_argument('id', ''))
        name = convert.bs2utf8(self.get_argument('name', ''))
        cardcode = convert.bs2utf8(self.get_argument('cardcode', ''))
        describe = convert.bs2utf8(self.get_argument('describe', ''))
        result = {}
        if name:
            result.update({"name": name})
        if cardcode:
            result.update({"cardcode": cardcode})
        if describe:
            result.update({"describe": describe})
        return id, result

    def _get_grade_argument(self):
        id = convert.bs2utf8(self.get_argument('id', ''))
        name = convert.bs2utf8(self.get_argument('name', ''))
        school_id = convert.bs2utf8(self.get_argument('school_id', ''))
        result = {}
        if name:
            result.update({"name": name})
        if school_id:
            result.update({"school_id": school_id})
        return id, result

    def _get_class_argument(self):
        id = convert.bs2utf8(self.get_argument('id', ''))
        name = convert.bs2utf8(self.get_argument('name', ''))
        grade_id = convert.bs2utf8(self.get_argument('grade_id', ''))
        cardcode = convert.bs2utf8(self.get_argument('cardcode', ''))
        describe = convert.bs2utf8(self.get_argument('describe', ''))
        student_number = int(self.get_argument('study_number', 0))
        result = {}
        if name:
            result.update({"name": name})
        if grade_id:
            result.update({"grade_id": grade_id})
        if cardcode:
            result.update({"cardcode": cardcode})
        if describe:
            result.update({"describe": describe})
        if student_number:
            result.update({"student_number": student_number})
        return id, result

    def _get_teacher_argument(self):
        id = convert.bs2utf8(self.get_argument('id', ''))
        name = convert.bs2utf8(self.get_argument('name', ''))
        sex = int(self.get_argument('sex', 0))
        birthday = convert.bs2utf8(self.get_argument('birthday', ""))
        class_id = convert.bs2utf8(self.get_argument('class_id', ''))
        phone = convert.bs2utf8(self.get_argument('phone', ''))
        describe = convert.bs2utf8(self.get_argument('describe', ''))
        result = {}
        if name:
            result.update({"name": name})
        if sex:
            result.update({"sex": sex})
        if birthday:
            result.update({"birthday": birthday})
        if class_id:
            result.update({"class_id": class_id})
        if phone:
            result.update({"phone": phone})
        if describe:
            result.update({"describe": describe})
        return id, result


    def _get_student_argument(self):
        id = convert.bs2utf8(self.get_argument('id', ''))
        name = convert.bs2utf8(self.get_argument('name', ''))
        sex = int(self.get_argument('sex', 0))
        birthday = convert.bs2utf8(self.get_argument('birthday', ""))
        class_id = convert.bs2utf8(self.get_argument('class_id', ''))
        status = convert.bs2utf8(self.get_argument('status', ''))
        relation_number = int(self.get_argument('relation_number', 3))
        describe = convert.bs2utf8(self.get_argument('describe', ''))
        result = {}
        if name:
            result.update({"name": name})
        if sex:
            result.update({"sex": sex})
        if birthday:
            result.update({"birthday": birthday})
        if class_id:
            result.update({"class_id": class_id})
        if status:
            result.update({"status": status})
        if relation_number:
            result.update({"relation_number": relation_number})
        if describe:
            result.update({"describe": describe})
        return id, result

    def _get_relative_argument(self):
        id = convert.bs2utf8(self.get_argument('id', ''))
        name = convert.bs2utf8(self.get_argument('name', ''))
        sex = int(self.get_argument('sex', 0))
        birthday = convert.bs2utf8(self.get_argument('birthday', 0))
        phone = convert.bs2utf8(self.get_argument('phone', ''))
        describe = convert.bs2utf8(self.get_argument('describe', ''))
        result = {}
        if name:
            result.update({"name": name})
        if sex:
            result.update({"sex": sex})
        if birthday:
            result.update({"birthday": birthday})
        if phone:
            result.update({"phone": phone})
        if describe:
            result.update({"describe": describe})
        return id, result

    def _get_relation_argument(self):
        id = convert.bs2utf8(self.get_argument('id', ''))
        relation = convert.bs2utf8(self.get_argument('relation', ''))
        student_id = convert.bs2utf8(self.get_argument('student_id', ''))
        relative_id = convert.bs2utf8(self.get_argument('relative_id', ''))
        result = {
            "relation": relation,
            "student_id": student_id,
            "relative_id": relative_id
        }
        return id, result

    def _get_user_argument(self):
        name = convert.bs2utf8(self.get_argument('name', ''))
        level = int(self.get_argument('level', -1))
        school_id = convert.bs2utf8(self.get_argument('school_id', ''))
        phone = convert.bs2utf8(self.get_argument('phone', ''))
        result = {}
        if name:
            result.update({"name": name,})
        if school_id:
            result.update({"school_id": school_id})

        #only admin
        current_user_level = self.get_secure_cookie('user_level', "")
        if current_user_level == "0" and level>-1:
            result.update({"level": level})
        if phone:
            result.update({"phone": phone})
        return id, result

