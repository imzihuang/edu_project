#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import randint
import datetime
from util.encrypt_md5 import encry_md5
from util import convert
from util.exception import ParamExist, NotFound, ParamNone, FormalError
from db import api as db_api
from logic import Logic
import logging
LOG = logging.getLogger(__name__)

class UserLogic(Logic):
    def __init__(self):
        super(UserLogic, self).__init__()

    def views(self, models):
        if isinstance(models, dict):
            models.pop("pwd")
            return models
        if isinstance(models, list):
            result = []
            for model in models:
                _model = model.to_dict()
                _model.pop("pwd")
                result.append(_model)
            return result
        model = models.to_dict()
        model.pop("pwd")
        return model

    def input(self, name="", pwd="", affirm_pwd="", activate=0, phone="", school_id="", level=1):
        if pwd != affirm_pwd:
            raise FormalError(pwd=pwd, affirm_pwd=affirm_pwd)
        if not convert.is_mobile(phone):
            raise FormalError(phone=phone)
        if db_api.user_list(name=name):
            raise ParamExist(key="name", value=name)
        if db_api.user_list(phone=phone):
            raise ParamExist(key="phone", value=phone)
        values = {
            "name": name,
            "pwd": encry_md5(pwd.strip()),
            "activate": activate,
            "phone": phone,
            "level": level
        }
        if school_id:
            if not db_api.school_get(school_id):
                raise NotFound(school_id=school_id)
            values.update({"school_id": school_id})
        user_obj = db_api.user_create(values)
        return user_obj

    def update(self, id="", **kwargs):
        if not id or not kwargs:
            raise ParamNone(id=id)
        LOG.info("kwargs 111:%r"%kwargs)
        user_info = db_api.user_get(id)
        current_user_level = kwargs.pop("current_user_level")
        if not user_info or current_user_level >= user_info.level:
            raise FormalError(current_user_level=current_user_level, level=user_info.level)

        if kwargs.get("school_id", ""):
            _ = db_api.school_get(kwargs.get("school_id", ""))
            if not _:
                raise NotFound(school_id=kwargs.get("school_id", ""))
        name = kwargs.get("name", "")
        if name and user_info.name!=name and db_api.user_list(name=name):
            raise ParamExist(key="name", value=name)
        phone = kwargs.get("phone", "")
        LOG.info("kwargs 333:%r" % kwargs)
        if phone and user_info.phone!=phone and db_api.user_list(phone=phone):
            raise ParamExist(key="phone", value=phone)
        if kwargs.get("pwd", ""):
            kwargs.pop("pwd")
        LOG.info("kwargs 444:%r" % kwargs)
        _ = db_api.user_update(id, kwargs)
        return _

    def update_pwd_by_phone(self, phone, pwd):
        user_list = db_api.user_list(phone=phone)
        if not user_list:
            return False
        user_id = user_list[0].id
        if not phone:
            return False
        if not convert.is_mobile(phone):
            return False
        db_api.user_update(user_id, {"pwd":encry_md5(pwd.strip())})
        return True


    def infos(self, id="", name="", phone="", school_id="", limit=100, offset=1):
        offset = (offset - 1) * limit if offset > 0 else 0
        filters = dict()
        if id:
            filters.update({"id": id})
        if name:
            filters.update({"name": name})
        if phone:
            filters.update({"phone": phone})
        if school_id:
            filters.update({"school_id": school_id})
        user_list = db_api.user_list(offset=offset, limit=limit, **filters)
        user_count = db_api.user_count(**filters)
        user_views = self.views(user_list)
        for user_info in user_views:
            school_info = db_api.school_get(id=user_info.get("school_id"))
            if school_info:
                user_info.update({"school_name": school_info.name})

        return {"count": user_count, "state": 0, "message": "query success", "data": user_views}


    def auth_username(self, name, pwd):
        filters = {
            "name": name,
            "pwd": encry_md5(pwd)
        }
        user_list = db_api.user_list(**filters)
        if user_list:
            user_info = self.views(user_list[0])
            if user_info.get("school_id", ""):
                school_info = db_api.school_get(user_info.get("school_id"))
                user_info.update({"school_name": school_info.name})
                user_info.update({"cardcode": school_info.cardcode})
            return user_info

    def auth_phone(self, phone, pwd):
        user_list = db_api.user_list(phone=phone, pwd=encry_md5(pwd))
        if user_list:
            user_info = self.views(user_list[0])
            if user_info.get("school_id", ""):
                school_info = db_api.school_get(user_info.get("school_id"))
                user_info.update({"school_name": school_info.name})
                user_info.update({"cardcode": school_info.cardcode})
            return user_info

    def delete(self, id="", **kwargs):
        user_list = db_api.user_list(id=id)
        if not user_list:
            return "Id does not exist"
        current_user_level = kwargs.pop("current_user_level")
        for user_info in user_list:
            if int(current_user_level) >= user_info.level:
                return "Permissions cannot be deleted"
        db_api.user_deleted(id=id)

class WXUserLogic(Logic):
    def __init__(self):
        super(WXUserLogic, self).__init__()

    def input(self, openid="", session_key="", phone="", wx_type=1):
        if db_api.wxuser_list(openid=openid):
            raise ParamExist(key="openid", value=openid)

        if db_api.wxuser_list(session_key=session_key):
            raise ParamExist(key="session_key", value=session_key)

        values = {
            "openid": openid,
            "session_key": session_key,
            "wx_type": wx_type
        }
        if phone and convert.is_mobile(phone):
            values.update({"phone": phone})

        wx_obj = db_api.wxuser_create(values)
        return wx_obj

    def update(self, id="", **kwargs):
        if not id or not kwargs:
            return False
        _ = db_api.wxuser_update(id, kwargs)
        return _

    def infos(self, id="", openid="", phone="", limit=100, offset=1):
        offset = (offset - 1) * limit if offset > 0 else 0
        filters = dict()
        if id:
            filters.update({"id": id})
        if openid:
            filters.update({"openid": openid})
        if phone:
            filters.update({"phone": phone})
        wx_list = db_api.wxuser_list(offset=offset, limit=limit, **filters)
        wx_count = db_api.wxuser_count(**filters)
        return {"count": wx_count, "state": 0, "message": "query success", "data": self.views(wx_list)}

    def info(self, id):
        if not id:
            return
        wx_info = db_api.wxuser_get(id)
        return self.views(wx_info)

    def info_by_phone(self, phone):
        if not phone:
            return
        wx_info = db_api.wxuser_get_by_phone(phone)
        return self.views(wx_info)

    def info_by_openid(self, openid):
        if not openid:
            return
        wx_infos = db_api.wxuser_list(openid=openid)
        if wx_infos:
            return self.views(wx_infos[0])

    def delete(self, id="", **kwargs):
        if not id:
            return "id is none"
        db_api.wxuser_deleted(id=id)



