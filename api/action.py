#coding:utf-8

from tornado.web import RequestHandler
import base64
import logging
import json
import os
from PIL import Image
from logic.userlogic import UserLogic
from logic.facelogic import FaceLogic
from util.ini_client import ini_load
from util.face_recognition_api import face_recognition_yyl
from util import common_util

LOG = logging.getLogger(__name__)

_conf = ini_load('config/service.ini')
_dic_con = _conf.get_fields('face++')
face_api_key = _dic_con.get("api_key", "")
face_api_secret = _dic_con.get("api_secret", "")
face_detect_url = _dic_con.get("detect_url", "")

class ActionHandler(RequestHandler):
    def initialize(self, static_path, face_path, tmp_path, **kwds):
        self.static_path = static_path
        self.face_path = face_path
        self.tmp_path = tmp_path

    def post(self, action):
        if action == "login":
            self.login()
            return
        if action == "auth":
            self.face_auth()
            return

        if action == "face_signin":
            self.face_signin()
            return

        if action == "face_signout":
            self.face_signout()
            return


    def login(self):
        level = int(self.get_argument('level', 0))
        name = self.get_argument('name', '')
        pwd = self.get_argument('pwd', '')
        phone = self.get_argument('phone', '')
        _op = UserLogic()
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

    def img_resize(self, path):
        """
        对大于2M的图片进行缩放
        :param path:
        :return:
        """
        fsize = os.path.getsize(path)
        if fsize <= 2097152:
            return
        ims = Image.open(path)
        s = 1920
        w = ims.width / s
        h = ims.height / s
        if w > h:
            width = s
            height = int(s * (h / w))
        else:
            height = s
            width = int(s * (w / h))

        ims = ims.resize((width, height))
        ims.save(path)

    def face_auth(self):
        relevance_id = self.get_argument('relevance_id', '')
        relevance_type = int(self.get_argument('relevance_id', 1))
        school_id = self.get_argument('school_id', '')
        if not relevance_id:
            self.finish(json.dumps({'state': 1, 'message': 'relevance_id is None'}))
            return
        # 将图片存储到本地
        img = self.get_argument('image', '')
        file_path = self.static_path + self.face_path + relevance_id + '.jpg'
        with open(file_path, 'wb') as up:
             up.write(base64.b64decode(img.rpartition(",")[-1]))

        self.img_resize(file_path)

        # 通过第三方api获取人脸特征
        #identy_code, face_token = face_util.face_identy(file_path)
        code, face_token = face_recognition_yyl.Face_Detect(file_path)
        if code != 200:
            LOG.error("detect face error:%s"%code)
            self.finish(json.dumps({'state': 2, 'message': face_token}))
            return

        # 将特征写入数据库
        code, faceset_token = face_recognition_yyl.Face_Add(school_id, face_token)
        if code != 200:
            LOG.error("add face error:%s" % code)
            self.finish(json.dumps({'state': 2, 'message': face_token}))
            return

        _op = FaceLogic()
        _op.create_face(school_id, relevance_id, face_token, faceset_token, relevance_type=relevance_type)
        self.finish(json.dumps({'state': 0, 'message': 'face auth ok'}))


    def face_signin(self):
        cardcode = self.get_argument('cardcode', '')
        features = self.get_argument('features', '')
        tmp_id = common_util.create_id()
        if not cardcode:
            self.finish(json.dumps({'state': 1, 'message': 'cardcode is None'}))
            return
        # 将图片存储到本地
        img = self.get_argument('image', '')
        file_path = self.static_path + self.tmp_path + tmp_id + '.jpg'
        with open(file_path, 'wb') as up:
            up.write(base64.b64decode(img.rpartition(",")[-1]))

    def face_signout(self):
        cardcode = self.get_argument('cardcode', '')
        features = self.get_argument('features', '')

        # 验证下通过，将签到信息写入数据库

        # 验证不通过，提示重新签退

