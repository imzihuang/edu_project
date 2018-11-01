#coding:utf-8

from tornado.web import RequestHandler
import json
from util.convert import is_mobile
from util.exception import ParamExist
import logging

from logic import Logic
from logic.school import SchoolLogic
from logic.classlogic import ClassLogic
from logic.teacher import TeacherLogic
from logic.student import StudentLogic
from logic.relative import RelativeLogic
from logic.relation import RelationLogic

LOG = logging.getLogger(__name__)

class DeleteHandler(RequestHandler):
    def post(self, delete_obj):
        try:
            pass
        except Exception as ex:
            LOG.error("Delete %s error:%s" % (delete_obj, ex))
            self.finish(json.dumps({'state': 10, 'message': 'Delete action error'}))
