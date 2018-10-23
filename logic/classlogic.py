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

    def intput(self, name="", grade="", school_id="", study_number=""):
        values = {
            "name": name,
            "grade": grade,
            "school_id": school_id,
            "study_number": study_number
        }
        class_obj = db_api.class_create(values)
        return class_obj

    def update(self, id="", **kwargs):
        if not id or not kwargs:
            return False
        _ = db_api.class_update(id, kwargs)
        return _

    def infos(self, id="", name="", school_id="", school_name="", grade="", limit=100, offset=1):
        offset = (offset - 1) * limit if offset > 0 else 0
        filters = dict()
        if id:
            filters.update({"id": id})
        if name:
            filters.update({"name": name})
        if school_id or school_id:
            if school_name:
                _school_list = db_api.school_list(name=school_name)
                if not _school_list:
                    return {"count": 0, "state": 0, "message": "query success", "data": []}
                school_id = _school_list[0].id
            filters.update({"school_id": school_id})

        if grade:
            filters.update({"grade": grade})

        class_list = db_api.class_list(offset=offset, limit=limit, **filters)
        class_count = db_api.class_count(**filters)
        return {"count": class_count, "state": 0, "message": "query success", "data": self.views(class_list)}