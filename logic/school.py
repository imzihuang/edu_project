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
        return school_obj

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
        LOG.info("11111111111111111111")

        school_list = db_api.school_list(offset=offset, limit=limit, **filters)
        LOG.info("11111111111111111111%r"%school_list)
        school_count = db_api.school_count(**filters)
        return {"count": school_count, "state": 0, "message": "query success", "data": self.views(school_list)}