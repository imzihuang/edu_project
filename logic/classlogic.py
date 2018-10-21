#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import randint
import datetime
from util.convert import *
from db import api as db_api
from logic import Logic

class ClassLogic(Logic):
    def __init__(self):
        pass

    def intput(self, name="", grade="", school_code="", study_number=""):
        values = {
            "name": name,
            "grade": grade,
            "school_code": school_code,
            "study_number": study_number
        }
        class_obj = db_api.class_create(values)
        return class_obj

    def update(self, code="", **kwargs):
        if not code or not kwargs:
            return False
        _ = db_api.class_update(code, kwargs)
        return _

    def infos(self, code="", name="", school_code="", school_name="", grade="", limit=100, offset=1):
        offset = (offset - 1) * limit if offset > 0 else 0
        filters = dict()
        if code:
            filters.update({"code": code})
        if name:
            filters.update({"name": name})
        if school_code or school_name:
            if school_name:
                _school_list = db_api.school_list(name=school_name)
                if not _school_list:
                    return {"count": 0, "state": 0, "message": "query success", "data": []}
                school_code = _school_list[0].code
            filters.update({"school_code": school_code})

        if grade:
            filters.update({"grade": grade})

        class_list = db_api.class_list(offset=offset, limit=limit, **filters)
        class_count = db_api.class_count(**filters)
        return {"count": class_count, "state": 0, "message": "query success", "data": class_list}