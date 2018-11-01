#coding:utf-8

from tornado.web import RequestHandler
import base64
import logging
import json
from logic.userlogic import UserLogic
from logic.relative import RelativeLogic
from util.ini_client import ini_load
import os
from PIL import Image
import requests

LOG = logging.getLogger(__name__)

_conf = ini_load('config/service.ini')



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
            self.face_identy()
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
        #对大于2M的图片进行缩放
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

    def face_identy(self):
        relative_id = self.get_argument('relative_id', '')
        if not relative_id:
            self.finish(json.dumps({'state': 1, 'message': 'relative_code is None'}))
            return
        # 获取用户上传的数据
        img = self.get_argument('image', '')
        file_path = self.static_path + self.face_path + relative_id + '.jpg'
        with open(file_path, 'wb') as up:
             up.write(base64.b64decode(img.rpartition(",")[-1]))

        # 通过第三方api获取人脸特征
        #img.save(file_path) #保存用户的图片
        self.img_resize(file_path)
        files = {'image_file':open(file_path,'rb').read()}
        api_key = 'd7KyrJBh3NQeFfsUaQCaVMvkHeYykU0p'
        api_secret = 't4WbsJTPLo5XOquBlS2q8bNHJEJstzP3'
        #人脸检测
        detect_url = 'https://api-cna.faceplusplus.com/facepp/v3/detect'
        data = {
            'api_key':api_key,
            'api_secret':api_secret,
        }
        response = requests.post(detect_url,data=data,files=files)
        results = response.json()
        if results.get('error_message'):
            self.finish(json.dumps({'state': 2, 'message': results.get('error_message')}))
            return

        face_token = results['faces'][-1]['face_token']
        #将特征写入数据库
        _op = RelativeLogic()
        _op.update(relative_id, face_token = face_token)
        self.finish(json.dumps({'state': 0, 'message': 'face identy ok'}))


    def face_signin(self):
        cardcode = self.get_argument('cardcode', '')
        features = self.get_argument('features', '')

        #验证下通过，将签到信息写入数据库

        #验证不通过，提示重新签到

    def face_signout(self):
        cardcode = self.get_argument('cardcode', '')
        features = self.get_argument('features', '')

        # 验证下通过，将签到信息写入数据库

        # 验证不通过，提示重新签退

