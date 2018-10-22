#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import randint
import datetime
from util.convert import *
from db import api as db_api
from logic import Logic

class RelativeLogic(Logic):

    def intput(self, name="", sex=0, age=0, student_id="", relation="", phone=""):
        values = {
            "name": name,
            "sex": sex,
            "age": age,
            "student_id": student_id,
            "relation": relation,
            "phone": phone
        }
        relativel_obj = db_api.relative_create(values)
        return relativel_obj

    def update(self, id="", **kwargs):
        if not id or not kwargs:
            return False
        _ = db_api.relative_update(id, kwargs)
        return _

    def infos(self, id="", name="",
              school_id="", school_name="",
              student_id="", student_name="",
              phone="",
              limit=100, offset=1):
        offset = (offset - 1) * limit if offset > 0 else 0
        filters = dict()
        if id:
            filters.update({"id": id})
        if name:
            filters.update({"name": name})
        if school_id or school_name:
            if school_name:
                _school_list = db_api.school_list(name=school_name)
                if not _school_list:
                    return {"count": 0, "state": 0, "message": "query success", "data": []}
                school_id = _school_list[0].id
            filters.update({"school_id": school_id})
        if student_id or student_name:
            if student_name:
                _student_list = db_api.student_list(name=student_name)
                if not _student_list:
                    return {"count": 0, "state": 0, "message": "query success", "data": []}
                student_id = _student_list[0].id
            filters.update({"student_id": student_id})

        if phone:
            filters.update({"phone": phone})

        relative_list = db_api.relative_list(offset=offset, limit=limit, **filters)
        relative_count = db_api.relative_count(**filters)
        return {"count": relative_count, "state": 0, "message": "query success", "data": relative_list}