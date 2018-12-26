#coding:utf-8

from tornado.web import RequestHandler
import json
from util.exception import ParamExist
import logging

from util import convert
from util import util_excel
from util.exception import NotFound, ParamNone
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
            if combination == "student_sign_details":
                self.student_sign_details()
            if combination == "teacher_sign":
                self.teacher_sign()
            if combination == "teacher_sign_details":
                self.teacher_sign_details()
            if combination == "batch_student_excel":
                self.batch_student_excel()
        except NotFound as ex:
            LOG.error("combination info %s param not data:%s" % (combination, ex))
            self.finish(json.dumps({'state': 2, 'message': 'param not data'}))
        except ParamNone as ex:
            LOG.error("combination info %s param is None:%s" % (combination, ex))
            self.finish(json.dumps({'state': 3, 'message': 'param is None'}))
        except Exception as ex:
            LOG.error("combination %s error:%s"%(combination, ex))
            self.finish(json.dumps({'state': 10, 'message': 'combination info error'}))

    def student_sign(self):
        school_id = convert.bs2utf8(self.get_argument('school_id', ''))
        student_id = convert.bs2utf8(self.get_argument('student_id', ''))
        student_name = convert.bs2utf8(self.get_argument('student_name', ''))
        relative_id = convert.bs2utf8(self.get_argument('relative_id', ''))
        grade_id = convert.bs2utf8(self.get_argument('grade_id', ''))
        class_id = convert.bs2utf8(self.get_argument('class_id', ''))
        sign_date = convert.bs2utf8(self.get_argument('sign_date', ''))
        limit = int(self.get_argument('limit', 100))
        offset = int(self.get_argument('offset', 0))

        student_op = StudentLogic()
        _ = student_op.infos_for_sign(id=student_id, name=student_name,
                                      school_id=school_id,
                                      grade_id=grade_id, class_id=class_id,
                                      relative_id=relative_id, sign_date=sign_date,
                                      limit=limit, offset=offset
                                  )
        if _:
            self.finish(json.dumps(_))
        else:
            self.finish(json.dumps({'state': 1, 'message': 'action student_sign error'}))


    def student_sign_details(self):
        student_id = convert.bs2utf8(self.get_argument('student_id', ''))
        start_date = convert.bs2utf8(self.get_argument('start_date', ''))
        end_date = convert.bs2utf8(self.get_argument('end_date', ''))
        student_op = StudentLogic()
        _ = student_op.info_detail_for_sign(student_id, start_date, end_date)
        if _:
            self.finish(json.dumps(_))
        else:
            self.finish(json.dumps({'state': 1, 'message': 'action student_sign_details error'}))

    def teacher_sign(self):
        teacher_id = convert.bs2utf8(self.get_argument('teacher_id', ''))
        teacher_name = convert.bs2utf8(self.get_argument('teacher_name', ''))
        school_id = convert.bs2utf8(self.get_argument('school_id', ''))
        grade_id = convert.bs2utf8(self.get_argument('grade_id', ''))
        class_id = convert.bs2utf8(self.get_argument('class_id', ''))
        sign_date = convert.bs2utf8(self.get_argument('sign_date', ''))
        limit = int(self.get_argument('limit', 100))
        offset = int(self.get_argument('offset', 0))

        teacher_op = TeacherLogic()
        _ = teacher_op.infos_for_sign(teacher_id, teacher_name, school_id, grade_id, class_id, sign_date, limit, offset)

        if _:
            self.finish(json.dumps(_))
        else:
            self.finish(json.dumps({'state': 1, 'message': 'action student_sign error'}))

    def batch_student_excel(self):
        student_id = convert.bs2utf8(self.get_argument('student_id', ''))
        student_name = convert.bs2utf8(self.get_argument('student_name', ''))
        grade_id = convert.bs2utf8(self.get_argument('grade_id', ''))
        class_id = convert.bs2utf8(self.get_argument('class_id', ''))
        student_op = StudentLogic()

        _data = student_op.student_relative_excel(student_id, student_name, grade_id, class_id)
        _excel = util_excel.make_student_excel(_data)
        self.write(_excel)
        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition', 'attachment; filename=student.xls')
        self.finish()



