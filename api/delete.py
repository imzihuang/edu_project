#coding:utf-8

from tornado.web import RequestHandler
import json
from util.convert import is_mobile
from util.exception import ParamExist
import logging

from logic import Logic
from logic.gradelogic import GradeLogic
from logic.classlogic import ClassLogic
from logic.teacher import TeacherLogic
from logic.student import StudentLogic
from logic.relative import RelativeLogic
from logic.relation import RelationLogic
from logic.facelogic import FaceLogic

LOG = logging.getLogger(__name__)

class DeleteHandler(RequestHandler):
    def post(self, delete_obj):
        try:
            id = self.get_argument('id', '')
            _op = Logic()

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

            if not id:
                self.finish(json.dumps({'state': 9, 'message': 'params %s is None' % delete_obj}))
            id = id.split(",")
            _message = _op.delete(id)
            if _message:
                self.finish(json.dumps({'state': 8, 'message': _message}))
                return
            self.finish(json.dumps({'state': 0, 'message': 'delete info success.'}))
        except Exception as ex:
            LOG.error("Delete %s error:%s" % (delete_obj, ex))
            self.finish(json.dumps({'state': 10, 'message': 'Delete action error'}))
