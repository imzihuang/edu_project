#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import randint
import datetime
from util.convert import *
from db import api as db_api
from logic import Logic

class StudentLogic(Logic):
    def __init__(self):
        pass

    def intput(self, name="", sex=0, age=0, grade="", school_code="", class_code="", status="apply", relation_number=3):
        values = {
            "name": name,
            "sex": sex,
            "age": age,
            "grade": grade,
            "school_code": school_code,
            "class_code": class_code,
            "status": status,
            "relation_number": relation_number
        }
        student_obj = db_api.student_create(values)
        return student_obj

    def output(self):
        pass

    def infos(self, code="", name="", grade="",
              school_code="", school_name="",
              class_code="", class_name="",
              relative_code="", relative_name="",
              limit=100, offset=1):
        offset = (offset - 1) * limit if offset > 0 else 0
        filters = dict()
        if code:
            filters.update({"code": code})
        if name:
            filters.update({"name": name})
        if grade:
            filters.update({"grade": grade})
        if school_code or school_name:
            if school_name:
                _school_list = db_api.school_list(name=school_name)
                if not _school_list:
                    return {"count": 0, "state": 0, "message": "query success", "data": []}
                school_code = _school_list[0].code
            filters.update({"school_code": school_code})

        if class_code or class_name:
            if class_name:
                _class_list = db_api.class_list(name=class_name)
                if not _class_list:
                    return {"count": 0, "state": 0, "message": "query success", "data": []}
                class_code = _class_list[0].code
            filters.update({"class_code": class_code})
        if relative_code or relative_name:
            if relative_name:
                _relative_list = db_api.relative_list(name=relative_name)
                if not _relative_list:
                    return {"count": 0, "state": 0, "message": "query success", "data": []}
                relative_code = _relative_list[0].code
            filters.update({"relative_code": relative_code})

        student_list = db_api.student_list(offset=offset, limit=limit, **filters)
        student_count = db_api.student_count(**filters)
        return {"count": student_count, "state": 0, "message": "query success", "data": student_list}