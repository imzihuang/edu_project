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
    def post(self, combination):
        try:
            if combination == "student_relative":
                self.student_relative()
        except Exception as ex:
            LOG.error("combination %s error:%s"%(combination, ex))
            self.finish(json.dumps({'state': 2, 'message': 'combination input error'}))

    def check_student_relative(self):
        pass

    def student_relative(self):
        name = convert.bs2utf8(self.get_argument('name', ''))
        sex = int(self.get_argument('sex', 0))
        birthday = convert.bs2utf8(self.get_argument('birthday', ''))
        class_id = convert.bs2utf8(self.get_argument('class_id', ''))
        relation_number = int(self.get_argument('relation_number', 3))
        str_relative_list = convert.bs2utf8(self.get_argument('relative_list', '[]'))
        relative_list = json.loads(str_relative_list)

        LOG.info("str_relative_list:%s" % str_relative_list)
        LOG.info("relative_list:%r"%relative_list)

        #check params
        self.check_student_relative()

        stu_op = StudentLogic()
        relative_op = RelativeLogic()
        relation_op = RelationLogic()
        student_info = stu_op.input(name=name, sex=sex, birthday=birthday, class_id=class_id, relation_number=relation_number)
        if not student_info:
            self.finish(json.dumps({'state': 1, 'message': 'student info error'}))
            return
        for relative in relative_list:
            relative_info = relative_op.input(
                name=relative.get("name", ""),
                sex=relative.get("sex", 0),
                birthday=relative.get("birthday", ""),
                phone=relative.get("phone", ""))
            if not relative_info:
                self.finish(json.dumps({'state': 2, 'message': '%s: relative info error'%relative.get("name", "")}))
                return
            relation_info = relation_op.input(relative.get("relation", ""), student_id=student_info.get("id"), relative_id=relative_info.get("id"))
            if not relation_info:
                self.finish(json.dumps({'state': 3, 'message': '%s: relative info error' % relative.get("name", "")}))
                return
        self.finish(json.dumps({'state': 0, 'message': 'success'}))


