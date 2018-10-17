#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import randint
import datetime
from util.convert import *
from db import api as db_api
from logic import Logic

class SchoolLogic(Logic):
    def __init__(self):
        pass

    def intput(self, name="", cardcode="", describe=""):
        values = {
            "name": name,
            "cardcode": cardcode,
            "describe": describe
        }
        school_obj = db_api.school_create(values)
        return school_obj

    def update(self):
        pass

    def infos(self, code="", name="", cardcode="", limit=100, offset=1):
        offset = (offset-1)*limit if offset > 0 else 0
        filters = dict()
        if code:
            filters.update({"code": code})
        if name:
            filters.update({"name": name})
        if cardcode:
            filters.update({"cardcode": cardcode})

        school_list = db_api.school_list(offset=offset, limit=limit, **filters)
        school_count = db_api.school_count(**filters)
        return {"count": school_count, "state": 0, "message": "query success", "data": school_list}