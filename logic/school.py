#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import randint
import datetime
from util import convert
from util.exception import ParamExist
from util.ini_client import ini_load
from util.face_recognition_api import face_recognition_yyl
from db import api as db_api
from logic import Logic
import logging

LOG = logging.getLogger(__name__)

_conf = ini_load('config/service.ini')
_dic_con = _conf.get_fields('face++')
face_api_key = _dic_con.get("api_key", "")
face_api_secret = _dic_con.get("api_secret", "")
face_create_url = _dic_con.get("create_url", "")

class SchoolLogic(Logic):
    def input(self, name="", cardcode="", describe=""):
        if not name or not cardcode:
            LOG.error("school name or cardcode is None")
            return
        if db_api.school_list(name=name):
            raise ParamExist(name=convert.bs2unicode(name))
        values = {
            "name": name,
            "cardcode": cardcode,
            "describe": describe
        }
        school_obj = db_api.school_create(values)
        #生成人脸库，获取faceset_token，并更新学校
        #faceset_token = face_util.create_face_tokenset(values)
        code, faceset_token = face_recognition_yyl.FaceSet_Create(name, school_obj.get("id"))
        if code != 200:
            LOG.error("create faceset token error")
            return
        self.update(school_obj.get("id"), faceset_token=faceset_token)
        return values

    def update(self, id="", **kwargs):
        if not id or not kwargs:
            return False
        _ = db_api.school_update(id, kwargs)
        return _

    def infos(self, id="", name="", cardcode="", limit=100, offset=0):
        offset = (offset-1)*limit if offset > 0 else 0
        filters = dict()
        if id:
            filters.update({"id": id})
        if name:
            filters.update({"name": name})
        if cardcode:
            filters.update({"cardcode": cardcode})


        school_list = db_api.school_list(offset=offset, limit=limit, **filters)
        school_count = db_api.school_count(**filters)
        return {"count": school_count, "state": 0, "message": "query success", "data": self.views(school_list)}

    def delete(self, id="", **kwargs):
        if not id:
            return "id is none"
        relevance_grade_count = db_api.grade_count(school_id=id)
        if relevance_grade_count>0:
            return "exist grade"
        db_api.school_deleted(id=id)