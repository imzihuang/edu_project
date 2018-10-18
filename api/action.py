#coding:utf-8

from tornado.web import RequestHandler
from scipy import misc
import urllib
import re
import uuid
import tempfile
import Image
from util.convert import is_mobile
from util.face import RecognitionService
import logging

LOG = logging.getLogger(__name__)
IMAGE_TYPES = re.compile('image/(gif|p?jpeg|(x-)?png)')
ACCEPT_FILE_TYPES = IMAGE_TYPES

class ActionHandler(RequestHandler):
    def __init__(self, *args, **kwargs):
        super(ActionHandler, self).__init__(*args, **kwargs)
        model_checkpoint ='./model/20180920-153747'
        self.recognition_service = RecognitionService(model_checkpoint)

    def face_upload(self, relative_code):
        # 获取用户上传的数据
        img = self.request.files['image']
        file_path = self.application.settings.get('static_path') + 'image/face/' + relative_code + '.jpg'
        img.save(file_path)
        face_image = misc.imread(file_path, mode='RGB')
        # 人脸注册服务
        err_code, feature = self.recognition_service.register_face(face_image,relative_code)
        #将特征写入数据库

        return "ok"



    def post(self, action):
        if action == "login":
            pass
        if action == "identy":
            relative_code = self.get_argument('relative_code', '')
            message = self.handle_upload(relative_code)
            pass
        if action == "signin":
            cardcode = self.get_argument('cardcode', '')

            pass
        if action == "signout":
            cardcode = self.get_argument('cardcode', '')
            pass