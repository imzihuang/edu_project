#coding:utf-8

from tornado.web import RequestHandler
from scipy import misc
import urllib
from util.face import RecognitionService
import logging
import json
from logic.actionlogic import ActionLogic
from logic.relative import RelativeLogic
from util.ini_client import ini_load

LOG = logging.getLogger(__name__)

_conf = ini_load('config/service.ini')
_dic_con = _conf.get_fields('face_model')
try:
    recognition_service = RecognitionService(_dic_con.get("path"))
except Exception as ex:
    LOG.error("init face reconf error:%s"%ex)
    recognition_service = None


class ActionHandler(RequestHandler):
    def initialize(self, static_path, face_path, **kwds):
        #model_checkpoint ='./model/20180920-153747'
        self.static_path = static_path
        self.face_path = face_path

    def post(self, action):
        if action == "login":
            self.login()
            return
        if action == "identy":
            self.face_upload()
            return

        if action == "face_signin":
            cardcode = self.get_argument('cardcode', '')

            return
        if action == "face_signout":
            cardcode = self.get_argument('cardcode', '')
            return


    def login(self):
        level = int(self.get_argument('level', 0))
        name = self.get_argument('name', '')
        pwd = self.get_argument('pwd', '')
        phone = self.get_argument('phone', '')
        _op = ActionLogic()
        if name:
            if _op.auth_username(name, pwd):
                self.finish(json.dumps({'state': 0, 'message': 'user login success.'}))
            else:
                self.finish(json.dumps({'state': 1, 'message': 'user login error'}))
            return
        if level == 2 and phone:
            if _op.auth_teacher(phone, pwd):
                self.finish(json.dumps({'state': 0, 'message': 'teacher login success.'}))
            else:
                self.finish(json.dumps({'state': 1, 'message': 'teacher login error'}))
            return
        if level == 3 and phone:
            if _op.auth_relative(phone, pwd):
                self.finish(json.dumps({'state': 0, 'message': 'relative login success.'}))
            else:
                self.finish(json.dumps({'state': 1, 'message': 'relative login error'}))
            return
        self.finish(json.dumps({'state': 2, 'message': 'login fail'}))


    def face_upload(self):
        relative_id = self.get_argument('relative_id', '')
        if not relative_id:
            self.finish(json.dumps({'state': 1, 'message': 'relative_code is None'}))
            return
        # 获取用户上传的数据
        img = self.request.files['image']
        file_path = self.static_path + self.face_path + relative_id + '.jpg'
        img.save(file_path)
        face_image = misc.imread(file_path, mode='RGB')
        # 人脸注册服务
        err_code, feature = recognition_service.register_face(face_image, relative_id)
        #将特征写入数据库
        _op = RelativeLogic()
        if _op.auth_face_feature(relative_id, feature):
            self.finish(json.dumps({'state': 0, 'message': 'auth feature success.'}))
        else:
            self.finish(json.dumps({'state': 1, 'message': 'auth feature error'}))



