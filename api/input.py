#coding:utf-8

from tornado.web import RequestHandler
import json
from util.convert import is_mobile
import logging

LOG = logging.getLogger(__name__)

class RegistryHandler(RequestHandler):
    def _get_school_argument(self):
        name = self.get_argument('name', '')
        cardcode = self.get_argument('cardcode', '')
        describe = self.get_argument('describe', '')

    def _get_class_argument(self):
        name = self.get_argument('name', '')
        grade = self.get_argument('grade', '')
        school_code = self.get_argument('school_code', '')
        student_number = int(self.get_argument('study_number', 0))

    def _get_teacher_argument(self):
        name = self.get_argument('name', '')
        sex = int(self.get_argument('sex', 0))
        age = int(self.get_argument('age', 0))
        school_code = self.get_argument('school_code', '')
        class_code = self.get_argument('school_code', '')

    def _get_student_argument(self):
        name = self.get_argument('name', '')
        sex = int(self.get_argument('sex', 0))
        age = int(self.get_argument('age', 0))
        grade = self.get_argument('grade', '')
        class_code = self.get_argument('class_code', '')
        school_code = self.get_argument('school_code', '')
        status = self.get_argument('status', 'apply')
        relation_number = int(self.get_argument('school_code', 3))

    def _get_relative_argument(self):
        name = self.get_argument('name', '')
        sex = int(self.get_argument('sex', 0))
        age = int(self.get_argument('age', 0))
        student_code = self.get_argument('student_code', '')
        relation = self.get_argument('relation', '')
        phone = self.get_argument('phone', '')


    def _org_argument(self, registry_obj):
        if registry_obj == "school":
            return self._get_school_argument()
            pass

    def post(self, registry_obj):
        if registry_obj == "school":

            pass

        try:
            # 判断商家编号merchant_code

            # 验证运单号tracking_number

            # 验证手机号phone_number
            if not is_mobile(phone_number):
                self.finish(json.dumps({'state': 3, 'message': 'phone error'}))
                return
            express_op = express.Express()
            _ = express_op.intput(merchant_code, tracking_number, phone_number, dhl_code, remark)
            self.finish(json.dumps({'state': 0, 'message': 'input success'}))
        except Exception as ex:
            LOG.error("Input express error:%s"%ex)
            self.finish(json.dumps({'state': 4, 'message': 'input error'}))