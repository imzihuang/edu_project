#coding:utf-8

from tornado.web import RequestHandler
import json
from util.exception import ParamExist
import logging

from util import convert
from api.base_auth import auth_api_login
from logic.school import SchoolLogic
from logic.gradelogic import GradeLogic
from logic.classlogic import ClassLogic
from logic.teacher import TeacherLogic
from logic.student import StudentLogic
from logic.relative import RelativeLogic
from logic.relation import RelationLogic
from logic.teacher_history import Teacher_HistoryLogic
from logic.student_history import Student_HistoryLogic
from util import util_excel

LOG = logging.getLogger(__name__)

class CombinationHandler(RequestHandler):
    def initialize(self, static_path, excel_path, **kwds):
        self.static_path = static_path
        self.excel_path = excel_path

    @auth_api_login
    def post(self, combination):
        try:
            if combination == "student_relative":
                self.student_relative()
            if combination == "bath_update_relative":
                self.bath_update_relative()
            if combination == "delete_student_relative":
                self.delete_student_relative()
            if combination == "batch_teacher_excel":
                self.batch_teacher_excel()

        except Exception as ex:
            LOG.error("combination %s error:%s"%(combination, ex))
            self.finish(json.dumps({'state': 10, 'message': 'combination input error'}))

    def check_student_relative(self):
        name = convert.bs2utf8(self.get_argument('name', ''))
        birthday = convert.bs2utf8(self.get_argument('birthday', ''))
        class_id = convert.bs2utf8(self.get_argument('class_id', ''))
        str_relative_list = convert.bs2utf8(self.get_argument('relative_list', '[]'))
        relative_list = json.loads(str_relative_list)

        if birthday and not convert.is_date(birthday):
            return 1
        if not name:
            return 1
        if not class_id:
            raise 1

        relative_op = RelativeLogic()
        for relative_info in relative_list:
            relative_birthday = relative_info.get("birthday", "")
            if relative_birthday and not convert.is_date(convert.bs2utf8(relative_birthday)):
                return 2
            phone = convert.bs2utf8(relative_info.get("phone", ""))
            if phone and not convert.is_mobile(phone):
                return 2
            name = convert.bs2utf8(relative_info.get("name", ""))
            if not name:
                return 2
            if phone:
                db_relative_list = relative_op.info_by_phone(phone=phone)
                if db_relative_list and convert.bs2utf8(db_relative_list[0].get("name", "")) != name:
                    LOG.info("relative info, phone:%s and name:%s error"%(phone, name))
                    return 2


    def student_relative(self):
        name = convert.bs2utf8(self.get_argument('name', ''))
        sex = int(self.get_argument('sex', 0))
        birthday = convert.bs2utf8(self.get_argument('birthday', ''))
        class_id = convert.bs2utf8(self.get_argument('class_id', ''))
        relation_number = int(self.get_argument('relation_number', 3))
        str_relative_list = convert.bs2utf8(self.get_argument('relative_list', '[]'))
        relative_list = json.loads(str_relative_list)

        #check params
        _check = self.check_student_relative()
        if _check == 1:
            self.finish(json.dumps({'state': 1, 'message': 'student info error'}))
            return
        if _check == 2:
            self.finish(json.dumps({'state': 2, 'message': 'relative info error'}))
            return

        stu_op = StudentLogic()
        relative_op = RelativeLogic()
        relation_op = RelationLogic()
        student_info = stu_op.input(name=name, sex=sex, birthday=birthday, class_id=class_id, relation_number=relation_number)
        if not student_info:
            self.finish(json.dumps({'state': 1, 'message': 'student info error'}))
            return
        for relative in relative_list:
            relative_info = relative_op.input(
                name=convert.bs2utf8(relative.get("name", "")),
                sex=relative.get("sex", 0),
                birthday=convert.bs2utf8(relative.get("birthday", "")),
                phone=convert.bs2utf8(relative.get("phone", "")))
            if not relative_info:
                self.finish(json.dumps({'state': 2, 'message': '%s: relative info error'%relative.get("name", "")}))
                return
            relation_op.input(relative.get("relation", ""), student_id=student_info.get("id"), relative_id=relative_info.get("id"))
        self.finish(json.dumps({'state': 0, 'message': 'success'}))


    def bath_update_relative(self):
        message = ""
        student_id = convert.bs2utf8(self.get_argument('student_id', ''))
        relative_list = convert.bs2utf8(self.get_argument('relative_list', '[]'))
        relative_list = json.loads(relative_list)
        relative_op = RelativeLogic()
        relation_op = RelationLogic()
        for relative_info in relative_list:
            try:
                relative_id = relative_info.pop("id", "")
                relation = relative_info.pop("relation", "")
                if relative_id:
                    #update relative, relation
                    _ = relative_op.update(id=relative_id, **relative_info)
                    if not _:
                        message += "update relative error:%s" % relative_info.get("name", "")
                        continue
                    relation_info = relation_op.update(relative_id=relative_id, student_id=student_id, relation=relation)
                    if not relation_info:
                        message += "update relation error:%s, %s"%(relative_info.get("name", ""), relation)
                        continue
                else:
                    #add relative, relation
                    _ = relative_op.input(name=convert.bs2utf8(relative_info.get("name", "")),
                                          sex=relative_info.get("sex", 0),
                                          birthday=convert.bs2utf8(relative_info.get("birthday", "")),
                                          phone=convert.bs2utf8(relative_info.get("phone", "")))
                    if not _:
                        message += "add relative error:%s" % relative_info.get("name", "")
                        continue
                    relation_info = relation_op.input(relation, student_id=student_id, relative_id=_.get("id"))
                    if not relation_info:
                        message += "add relation error:%s, %s"%(relative_info.get("name", ""), relation)
                        continue
            except Exception as ex:
                LOG.error("update error: %s, %s"%(relative_info.get("name", ""), ex))
                message += "update error:%s" %relative_info.get("name", "")
        if not message:
            self.finish(json.dumps({'state': 0, 'message': 'update relative success'}))
        else:
            self.finish(json.dumps({'state': 1, 'message': message}))

    def delete_student_relative(self):
        student_id = convert.bs2utf8(self.get_argument('student_id', ''))
        stu_op = StudentLogic()
        stu_op.combination_delete(id=student_id)
        message = self.finish(json.dumps({'state': 0, 'message': 'success'}))
        if not message:
            self.finish(json.dumps({'state': 0, 'message': 'delete student success'}))
        else:
            self.finish(json.dumps({'state': 1, 'message': message}))

    def batch_teacher_excel(self):
        student_excels = self.request.files.get('student_excel', '')
        if not student_excels:
            LOG.error("student excel is none")
            self.finish(json.dumps({'state': 2, 'message': 'excel is none'}))
            return
        student_excel = student_excels[0]
        filename = student_excel['filename']
        filename = "teacher" + "." + filename.rpartition(".")[-1]
        file_path = self.static_path + self.excel_path + filename

        with open(file_path, 'wb') as up:
            up.write(student_excel['body'])

        teacher_data = util_excel.read_teacher_excel(file_path)
        teacher_op = TeacherLogic()
        _ = teacher_op.batch_input(teacher_data)
        if _[0]:
            self.finish(json.dumps({'state': 0, 'message': _[1]}))
        else:
            self.finish(json.dumps({'state': 1, 'message': _[1]}))









