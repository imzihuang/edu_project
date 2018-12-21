#coding:utf-8

from tornado.web import RequestHandler
import logging
import json
import os
import time
from PIL import Image
from api.base_auth import auth_api_login, set_edu_cookie
from logic.school import SchoolLogic
from logic.userlogic import UserLogic
from logic.facelogic import FaceLogic
from logic.signlogic import SignLogic
from logic.teacher import TeacherLogic
from logic.relative import RelativeLogic
from logic.verify_manage import VerifyManageLogic
from util.ini_client import ini_load
from util.face_recognition_api import face_recognition_yyl
from util import common_util, convert

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
        try:
            if action == "login":
                self.login()
                return

            if action == "sign_out":
                self.sign_out()
                return

            if action == "reset_pwd":
                self.reset_pwd()
                return

            if action == "face_auth":
                self.face_auth()
                return

            if action == "face_activate":
                self.face_activate()
                return

            if action == "face_disable":
                self.face_disable()
                return

            if action == "face_signin":
                self.face_signin()
                return

            if action == "push_verify":
                self.push_verify()
                return
        except Exception as ex:
            LOG.error("action %s error:%s" % (action, ex))
            self.finish(json.dumps({'state': 10, 'message': 'action error'}))


    def login(self):
        name = self.get_argument('name', '')
        pwd = self.get_argument('pwd', '')
        phone = self.get_argument('phone', '')
        _op = UserLogic()
        if name:
            user_info = _op.auth_username(name, pwd)
            if user_info:
                set_edu_cookie(self, user_info.get("name"), str(user_info.get("level")), user_info.get("school_id"))
                self.finish(json.dumps({'state': 0, 'message': 'user login success.', 'user_info': user_info}))
            else:
                self.finish(json.dumps({'state': 1, 'message': 'user login error'}))
            return
        if phone:
            user_info = _op.auth_phone(phone, pwd)
            if user_info:
                set_edu_cookie(self, user_info.get("name"), str(user_info.get("level")), user_info.get("school_id"))
                self.finish(json.dumps({'state': 0, 'message': 'phone login success.', 'user_info': user_info}))
            else:
                self.finish(json.dumps({'state': 1, 'message': 'phone login error'}))
            return

        self.finish(json.dumps({'state': 2, 'message': 'login fail'}))

    def sign_out(self):
        self.clear_cookie("user_name")
        self.clear_cookie("user_level")
        if self.get_secure_cookie('school_id'):
            self.clear_cookie("school_id")
        self.finish(json.dumps({'state': 0, 'message': 'logout ok'}))

    def reset_pwd(self):
        new_pwd = convert.bs2utf8(self.get_argument('new_pwd', ''))
        affirm_pwd = convert.bs2utf8(self.get_argument('affirm_pwd', ''))
        phone = convert.bs2utf8(self.get_argument('phone', ''))
        verify_code = convert.bs2utf8(self.get_argument('verify_code', ''))

        if not new_pwd or new_pwd != affirm_pwd:
            self.finish(json.dumps({'state': 1, 'message': 'pwd error'}))
            return

        verify_op = VerifyManageLogic()
        # verify code
        _ = verify_op.verify_code_phone(phone=phone, code=verify_code)
        if not _:
            self.finish(json.dumps({'state': 2, 'message': 'verify code error'}))
            return

        user_op = UserLogic()
        _ = user_op.update_pwd_by_phone(phone, new_pwd)
        if _:
            self.finish(json.dumps({'state': 0, 'message': 'reset pwd success'}))
        else:
            self.finish(json.dumps({'state': 3, 'message': 'reset pwd faild'}))

    def _img_resize(self, path):
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

    @auth_api_login
    def face_auth(self):
        relevance_id = convert.bs2utf8(self.get_argument('relevance_id', ''))
        relevance_type = int(self.get_argument('relevance_type', 1))
        school_id = convert.bs2utf8(self.get_argument('school_id', ''))
        alias = convert.bs2utf8(self.get_argument('alias', ''))
        if not relevance_id:
            self.finish(json.dumps({'state': 1, 'message': 'relevance_id is None'}))
            return

        if not school_id:
            if relevance_type == 2:
                #teacher
                teacher_op = TeacherLogic()
                teacher_info = teacher_op.info(relevance_id)
                school_id = teacher_info.get("school_id", "")
            if relevance_type in (1, 3):
                #relative
                relative_op = RelativeLogic()
                relative_info = relative_op.info(relevance_id)
                school_id = relative_info.get("school_id", "")


        face_op = FaceLogic()
        _verify = face_op.verify_authd(relevance_id, relevance_type)
        if _verify:
            LOG.error("The face token data has been stored.")
            self.finish(json.dumps({'state': 2, 'message': 'The face token has been stored.'}))
            return

        # 将图片存储到本地
        #img = self.get_argument('image', '')
        imgs = self.request.files.get('image', '')
        if not imgs:
            LOG.error("image is none")
            self.finish(json.dumps({'state': 3, 'message': 'image is none'}))
            return
        img = imgs[0]
        filename = img['filename']
        filename = relevance_id + "_" + str(int(time.time())) + "." + filename.rpartition(".")[-1]
        #file_path = self.static_path + self.face_path + relevance_id + '.jpg'
        file_path = self.static_path + self.face_path + filename
        LOG.info("file path:%s" % file_path)
        with open(file_path, 'wb') as up:
            up.write(img['body'])
             #up.write(base64.b64decode(img.rpartition(",")[-1]))

        self._img_resize(file_path)

        # 通过第三方api获取人脸特征
        #identy_code, face_token = face_util.face_identy(file_path)
        code, face_token = face_recognition_yyl.Face_Detect(file_path)
        if code != 200:
            LOG.error("detect face error:%s"%code)
            self.finish(json.dumps({'state': 4, 'message': face_token, 'code': code}))
            return

        # 将特征写入数据库
        code, faceset_token = face_recognition_yyl.Face_Add(school_id, face_token)
        if code != 200:
            LOG.error("add face error:%s" % code)
            self.finish(json.dumps({'state': 4, 'message': face_token, 'code': code}))
            return

        _ = face_op.input(school_id, relevance_id, face_token, faceset_token, filename, relevance_type=relevance_type, alias=alias)
        if _:
            self.finish(json.dumps({'state': 0, 'message': 'face auth ok'}))
        else:
            self.finish(json.dumps({'state': 5, 'message': 'face auth faild'}))

    @auth_api_login
    def face_activate(self):
        id = self.get_argument('id', '')
        face_op = FaceLogic()
        _ = face_op.activate(id)
        if _:
            self.finish(json.dumps({'state': 1, 'message': _}))
        else:
            self.finish(json.dumps({'state': 0, 'message': 'face active ok'}))

    @auth_api_login
    def face_disable(self):
        id = self.get_argument('id', '')
        face_op = FaceLogic()
        _ = face_op.disable(id)
        if _:
            self.finish(json.dumps({'state': 1, 'message': _}))
        else:
            self.finish(json.dumps({'state': 0, 'message': 'face disable ok'}))

    @auth_api_login
    def face_signin(self):
        cardcode = self.get_argument('cardcode', '')
        school_id = self.get_argument('school_id', '')
        face_img = self.request.files.get("image", None)
        tmp_id = common_util.create_id()
        if not face_img or not school_id:
            self.finish(json.dumps({'state': 1, 'message': 'school_id or img is None'}))
            return
        # 将图片存储到本地
        img = face_img[0]
        filename = tmp_id + ".jpg"
        file_path = self.static_path + self.tmp_path + filename

        LOG.info("file path:%s" % file_path)
        with open(file_path, 'wb') as up:
            up.write(img['body'])

        #获取tonken
        code, face_token = face_recognition_yyl.Face_Search(file_path, school_id)
        if code != 200:
            LOG.error("Search face error:%s" % code)
            self.finish(json.dumps({'state': 2, 'message': face_token, 'code': code}))
            return
        face_op = FaceLogic()
        sign_op = SignLogic()
        LOG.info("face token:%s"%face_token)

        face_list = face_op.verify_face(face_token, school_id, cardcode)
        if not face_list:
            self.finish(json.dumps({'state': 3, 'message': 'sign fail, face no exit'}))
        else:
            for face_info in face_list:
                sign_op.input(face_info.get("relevance_type", 1),
                              face_info.get("relevance_id", ""),
                              face_info.get("alias", ""),
                              filename,
                              face_info.get("img_path", ""))
            self.finish(json.dumps({'state': 0, 'message': 'sign ok'}))

    
    def push_verify(self):
        phone = convert.bs2utf8(self.get_argument('phone', ''))
        if not phone or not convert.is_mobile(phone):
            self.finish(json.dumps({'state': 1, 'message': 'Push verify code fail, phone is noe.'}))
            return
        verify_code = "888888"#common_util.create_verifycode()
        _op = VerifyManageLogic()
        _ = _op.input(phone=phone, verify_code=verify_code)
        if _:
            self.finish(json.dumps({'state': 0, 'message': 'Push verify code ok'}))
        else:
            self.finish(json.dumps({'state': 2, 'message': 'Push verify code fail'}))

