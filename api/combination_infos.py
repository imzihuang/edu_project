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

class CombinationHandler(RequestHandler):
    def get(self, combination):
        try:
            if combination == "student_sign":
                self.student_sign()

        except Exception as ex:
            LOG.error("combination %s error:%s"%(combination, ex))
            self.finish(json.dumps({'state': 10, 'message': 'combination input error'}))

    def student_sign(self):
        student_id = convert.bs2utf8(self.get_argument('student_id', ''))
        student_name = convert.bs2utf8(self.get_argument('student_name', ''))
        relative_id = convert.bs2utf8(self.get_argument('relative_id', ''))
        grade_id = convert.bs2utf8(self.get_argument('grade_id', ''))
        class_id = convert.bs2utf8(self.get_argument('class_id', ''))
        date =  convert.bs2utf8(self.get_argument('date', ''))
        limit = int(self.get_argument('limit', 100))
        offset = int(self.get_argument('offset', 1))

        student_op = StudentLogic()