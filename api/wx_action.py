#coding:utf-8

from tornado.web import RequestHandler
import tornado.httpclient
from six.moves.urllib import parse
from util.face import RecognitionService
import logging
import json
from logic.actionlogic import ActionLogic
from util.ini_client import ini_load

_conf = ini_load('config/service.ini')
_dic_con = _conf.get_fields('wx')

LOG = logging.getLogger(__name__)


class WXActionHandler(RequestHandler):
    def initialize(self, model_checkpoint, face_path, **kwds):
        #model_checkpoint ='./model/20180920-153747'
        self.recognition_service = RecognitionService(model_checkpoint)
        self.face_path = face_path

    def post(self, action):
        if action == "login":
            self.login()
            return
        if action == "bind":
            self.bind_user()
            return

    def login(self):
        code = int(self.get_argument('code', ''))
        app_id = _dic_con.get("appid")
        secret = _dic_con.get("secret")
        #https://api.weixin.qq.com/sns/jscode2session?appid=APPID&secret=SECRET&js_code=JSCODE&grant_type=authorization_code
        url = "https://api.weixin.qq.com/sns/jscode2session"
        params = {
            "appid": app_id,
            "secret": secret,
            "js_code": code,
            "grant_type": "authorization_code"
        }
        http_client = tornado.httpclient.HTTPClient()
        response = http_client.fetch("%s?%s"%(url, parse.urlencode(params)))
        dic_body = json.loads(response.body)
        openid = dic_body.get('openid')
        session_key = dic_body.get('session_key')
        #存储openid和session_key,并返回识别session串


        #_op = ActionLogic()

        self.finish(json.dumps({'state': 2, 'message': 'login fail'}))





