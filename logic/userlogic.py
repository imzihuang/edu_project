#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import randint
import datetime
from util.encrypt_md5 import encry_md5
from util.convert import *
from util.exception import ParamExist
from db import api as db_api
from logic import Logic
import logging
LOG = logging.getLogger(__name__)

class UserLogic(Logic):
    def __init__(self):
        super(UserLogic, self).__init__()

    def views(self, models):
        if isinstance(models, list):
            result = []
            for model in models:
                _ = model.to_dict().pop("pwd")
                result.append(_)
            return result
        _ = models.to_dict().pop("pwd")
        return _

    def intput(self, name="", pwd="", verify_code="", activate="",level=1):
        if db_api.user_list(name=name):
            raise ParamExist(key="name", value=name)
        values = {
            "name": name,
            "pwd": encry_md5(pwd),
            "verify_code": verify_code,
            "activate": activate,
            "level": level
        }
        user_obj = db_api.user_create(values)
        return self.views(user_obj)

    def update(self, id="", **kwargs):
        if not id or not kwargs:
            return False
        _ = db_api.user_update(id, kwargs)
        return _

    def infos(self,  id="", name="", limit=100, offset=1):
        offset = (offset - 1) * limit if offset > 0 else 0
        filters = dict()
        if id:
            filters.update({"id": id})
        if name:
            filters.update({"name": name})
        user_list = db_api.user_list(offset=offset, limit=limit, **filters)
        user_count = db_api.user_count(**filters)
        return {"count": user_count, "state": 0, "message": "query success", "data": self.views(user_list)}


    def auth_username(self, name, pwd):
        filters = {
            "name": name,
            "pwd": encry_md5(pwd)
        }
        _ = db_api.user_list(**filters)
        if _:
            return True
        return False

    def auth_teacher(self, phone, pwd):
        teacher_list = db_api.teacher_list(phone=phone)
        if teacher_list:
            user_id = teacher_list[0].user_id
            _ = db_api.user_list(id=user_id, pwd=encry_md5(pwd))
            if _:
                return True
        return False


    def auth_relative(self, phone, pwd):
        relative_list = db_api.relative_list(phone=phone)
        if relative_list:
            user_id = relative_list[0].user_id
            _ = db_api.user_list(id=user_id, pwd=encry_md5(pwd))
            if _:
                return True
        return False

    def delete(self, id="", **kwargs):
        db_api.user_deleted(id=id)

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
            filters.update({"openid": openid})
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

    def delete(self, id="", **kwargs):
        if not id:
            return
        db_api.wxuser_deleted(id=id)



