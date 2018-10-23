#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import randint
import datetime
from util.convert import *
from util.exception import ParamExist
from db import api as db_api
from logic import Logic
import logging
LOG = logging.getLogger(__name__)

class UserLogic(Logic):
    def __init__(self):
        super(UserLogic, self).__init__()

    def intput(self, ):
        pass

class WXUserLogic(Logic):
    def __init__(self):
        super(WXUserLogic, self).__init__()

    def intput(self, openid="", session_key="", phone=""):
        if db_api.wxuser_list(openid=openid):
            raise ParamExist(key="openid", value=openid)

        if db_api.wxuser_list(session_key=session_key):
            raise ParamExist(key="session_key", value=session_key)

        values = {
            "openid": openid,
            "session_key": session_key,
            "phone": phone
        }
        wx_obj = db_api.wxuser_create(values)
        return self.views(wx_obj)

    def update(self, id="", **kwargs):
        if not id or not kwargs:
            return False
        _ = db_api.wxuser_update(id, kwargs)
        return _

    def infos(self, id="", openid="", limit=100, offset=1):
        offset = (offset - 1) * limit if offset > 0 else 0
        filters = dict()
        if id:
            filters.update({"id": id})
        if openid:
            filters.update({"name": openid})
        wx_list = db_api.wxuser_list(offset=offset, limit=limit, **filters)
        wx_count = db_api.wxuser_count(**filters)
        return {"count": wx_count, "state": 0, "message": "query success", "data": self.views(wx_list)}

    def info(self, id):
        if not id:
            return
        wx_info = db_api.wxuser_get(id)
        return self.views(wx_info)

    def info_by_openid(self, openid):
        if not id:
            return
        wx_infos = db_api.wxuser_list(openid=openid)
        if wx_infos:
            return self.views(wx_infos[0])

