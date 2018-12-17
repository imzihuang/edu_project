#coding:utf-8

from tornado.web import RequestHandler
import json
import logging

from api.base_auth import auth_api_login
from logic import Logic
from logic.school import SchoolLogic
from logic.gradelogic import GradeLogic
from logic.classlogic import ClassLogic
from logic.teacher import TeacherLogic
from logic.student import StudentLogic
from logic.relative import RelativeLogic
from logic.relation import RelationLogic
from logic.facelogic import FaceLogic
from logic.userlogic import UserLogic

LOG = logging.getLogger(__name__)

class DeleteHandler(RequestHandler):
    @auth_api_login
    def post(self, delete_obj):
        try:
            id = self.get_argument('id', '')
            kwargs = {}
            _op = Logic()

            if delete_obj == "school":
                _op = SchoolLogic()

            if delete_obj == "grade":
                _op = GradeLogic()

            if delete_obj == "class":
                _op = ClassLogic()

            if delete_obj == "teacher":
                _op = TeacherLogic()

            if delete_obj == "student":
                _op = StudentLogic()

            if delete_obj == "relative":
                _op = RelativeLogic()

            if delete_obj == "relation":
                _op = RelationLogic()

            if delete_obj == "face":
                _op = FaceLogic()

            if delete_obj == "user":
                # only admin
                current_user_level = self.get_secure_cookie('user_level')
                if current_user_level != "0":
                    self.finish(json.dumps({'state': 2, 'message': 'only admin'}))
                    return
                kwargs.update({"current_user_level": current_user_level})
                _op = UserLogic()

            if not id:
                self.finish(json.dumps({'state': 1, 'message': 'params %s is None' % delete_obj}))
            id = id.split(",")
            _message = _op.delete(id, **kwargs)
            if _message:
                self.finish(json.dumps({'state': 9, 'message': _message}))
                return
            self.finish(json.dumps({'state': 0, 'message': 'delete info success.'}))
        except Exception as ex:
            LOG.error("Delete %s error:%s" % (delete_obj, ex))
            self.finish(json.dumps({'state': 10, 'message': 'Delete action error'}))
