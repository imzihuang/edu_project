#coding:utf-8

from tornado.web import RequestHandler
import tornado.httpclient
from six.moves.urllib import parse
from util.exception import ParamExist
import logging
import json
from logic.userlogic import WXUserLogic
from logic.relative import RelativeLogic
from logic.verify_manage import VerifyManageLogic
from util.ini_client import ini_load
from util import convert

_conf = ini_load('config/service.ini')
_dic_con = _conf.get_fields('wx')

LOG = logging.getLogger(__name__)


class WXActionHandler(RequestHandler):

    def post(self, action):
        try:
            if action == "login":
                self.login()
                return
            if action == "bind":
                self.bind_user()
                return
            if action == "update_user_phone":
                self.update_user_phone()
                return
            if action == "verify_phone_code":
                self.verify_phone_code()
                return
        except ParamExist as ex:
            LOG.error("Wx action %s error:%s" % (action, ex))
            self.finish(json.dumps({'state': 9, 'message': 'params exit'}))
        except Exception as ex:
            LOG.error("Wx action %s error:%s" % (action, ex))
            self.finish(json.dumps({'state': 10, 'message': 'wx action error'}))

    def login(self):
        code = self.get_argument('code', '')
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
        _op = WXUserLogic()
        exit_app = _op.info_by_openid(openid=openid)
        if exit_app:
            _op.update(exit_app.get("id"), session_key=session_key)
            self.finish(json.dumps({'state': 0, 'session_code': exit_app.get("id"), 'phone': exit_app.get("phone","")}))
        else:
            _ = _op.input(openid=openid, session_key=session_key)
            self.finish(json.dumps({'state': 0, 'session_code': _.get("id")}))

    def bind_user(self):
        phone = convert.bs2utf8(self.get_argument('phone', ''))
        verify_code = convert.bs2utf8(self.get_argument('verify_code', ''))
        edu_session = convert.bs2utf8(self.get_argument('edu_session', ''))
        relative_op = RelativeLogic()
        verify_op = VerifyManageLogic()
        wx_op = WXUserLogic()

        #verify code
        _ = verify_op.verify_code_phone(phone=phone, code=verify_code)
        if not _:
            LOG.error("bind user verify code error: phone:%s" % phone)
            self.finish(json.dumps({'state': 1, 'message': 'verify code error'}))
            return

        #verify relative
        relative_list = relative_op.info_by_phone(phone=phone)
        if not relative_list:
            LOG.error("bind user phone not singn relative: phone:%s" % phone)
            self.finish(json.dumps({'state': 2, 'message': 'phone not singn relative'}))
            return
        relative_ids = ",".join([relative_info.id for relative_info in relative_list])
        #verify phone exit
        old_wx_info = wx_op.info_by_phone(phone)
        if old_wx_info:
            LOG.error("bind user phone exit: phone:%s" % phone)
            self.finish(json.dumps({'state': 3, 'message': 'phone exit'}))
            return

        #bind phone
        wx_op.update(edu_session, phone=phone)
        self.finish(json.dumps(
            {'state': 0, 'edu_session': edu_session, 'relative_id': relative_ids, 'message': 'ok'}))


    def update_user_phone(self):
        phone = convert.bs2utf8(self.get_argument('phone', ''))
        verify_code = convert.bs2utf8(self.get_argument('verify_code', ''))
        edu_session = convert.bs2utf8(self.get_argument('edu_session', ''))
        relative_op = RelativeLogic()
        verify_op = VerifyManageLogic()
        wx_op = WXUserLogic()

        # verify code
        _ = verify_op.verify_code_phone(phone=phone, code=verify_code)
        if not _:
            self.finish(json.dumps({'state': 1, 'message': 'verify code error'}))
            return
        old_wx_info = wx_op.info(edu_session)
        if not old_wx_info:
            LOG.error("update user wx id not singn: phone:%s" % phone)
            self.finish(json.dumps({'state': 3, 'message': 'wx id not singn'}))
            return

        #验证待绑定手机号，是否被占用（微信号认证过，或者家属占用）
        verify_wx_info = wx_op.info_by_phone(phone)
        if verify_wx_info:
            LOG.error("update user phone, new phone exit wx: phone:%s" % phone)
            self.finish(json.dumps({'state': 3, 'message': 'new phone exit wx'}))
            return
        verify_relative_list = relative_op.info_by_phone(phone=phone)
        if verify_relative_list:
            LOG.error("update user phone, new phone exit relative: phone:%s" % phone)
            self.finish(json.dumps({'state': 3, 'message': 'new phone exit relative'}))
            return

        #待更新手机号码的亲属，通过旧手机号(可能存在多个)
        old_relative_list = relative_op.info_by_phone(phone=old_wx_info.get("phone"))
        if not old_relative_list:
            LOG.error("update user phone not singn: phone:%s" % phone)
            self.finish(json.dumps({'state': 2, 'message': 'old phone not singn'}))
            return

        relative_ids = ",".join([relative_info.id for relative_info in old_relative_list])
        for relative_info in old_relative_list:
            relative_op.update(relative_info.id, phone=phone)
        #更新微信号的手机号码
        wx_op.update(edu_session, phone=phone)
        self.finish(json.dumps({'state': 0, 'edu_session': edu_session, 'relative_id': relative_ids, 'message': 'ok'}))

    def verify_phone_code(self):
        phone = convert.bs2utf8(self.get_argument('phone', ''))
        verify_code = convert.bs2utf8(self.get_argument('verify_code', ''))
        verify_op = VerifyManageLogic()

        # verify code
        _ = verify_op.verify_code_phone(phone=phone, code=verify_code)
        if not _:
            self.finish(json.dumps({'state': 1, 'message': 'verify code error'}))
        else:
            self.finish(json.dumps({'state': 0, 'message': 'verify code ok'}))
