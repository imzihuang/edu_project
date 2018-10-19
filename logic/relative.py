#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import randint
import datetime
from util.convert import *
from db import api as db_api
from logic import Logic

class RelativeLogic(Logic):
    def __init__(self):
        pass

    def intput(self, name="", sex=0, age=0, student_code="", relation="", phone=""):
        values = {
            "name": name,
            "sex": sex,
            "age": age,
            "student_code": student_code,
            "relation": relation,
            "phone": phone
        }
        relativel_obj = db_api.relative_create(values)
        return relativel_obj

    def output(self):
        pass

    def infos(self, code="", name="",
              school_code="", school_name="",
              student_code="", student_name="",
              phone="",
              limit=100, offset=1):
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
        if student_code or student_name:
            if student_name:
                _student_list = db_api.student_list(name=student_name)
                if not _student_list:
                    return {"count": 0, "state": 0, "message": "query success", "data": []}
                student_code = _student_list[0].code
            filters.update({"student_code": student_code})

        if phone:
            filters.update({"phone": phone})

        relative_list = db_api.relative_list(offset=offset, limit=limit, **filters)
        relative_count = db_api.relative_count(**filters)
        return {"count": relative_count, "state": 0, "message": "query success", "data": relative_list}