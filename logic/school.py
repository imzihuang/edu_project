#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import randint
import datetime
from util.convert import *
from util.exception import ParamExist
from db import api as db_api
from logic import Logic
import logging
import requests

LOG = logging.getLogger(__name__)

class SchoolLogic(Logic):

    def intput(self, name="", cardcode="", describe=""):
        if not name or not cardcode:
            LOG.error("school name or cardcode is None")
            return False
        if db_api.school_list(name=name):
            raise ParamExist(key="name", value=name)
        values = {
            "name": name,
            "cardcode": cardcode,
            "describe": describe
        }
        school_obj = db_api.school_create(values)
        #生成人脸库，获取faceset_token，并更新学校
        if school_obj:
            api_key ='5ohw3BxhITBcWer8_0HY4ezXkX_xvESY'
            api_secret ='zOp9msYNAeBvjeQGgIygfHih8Jmn9vGM'
            #人脸库创建
            faceset_url = 'https://api-cn.faceplusplus.com/facepp/v3/faceset/create'
            data ={
            'api_key': api_key,
            'api_secret': api_secret,
           'display_name':name,
            'outer_id':values.get("id"),
            'tags':values.get("id"),
            }
            response = requests.post(faceset_url, data)
            results = response.json()
            if results.get('error_message'):
                pass
            else:
                faceset_token = results['faceset_token']  #faceset
                self.update(values.get("id"), faceset_token=faceset_token)
        return values

    def update(self, id="", **kwargs):
        if not id or not kwargs:
            return False
        _ = db_api.school_update(id, kwargs)
        return _

    def infos(self, id="", name="", cardcode="", limit=100, offset=1):
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
