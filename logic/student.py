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

    def intput(self, name="", sex=0, age=0, grade="", school_id="", class_id="", status="apply", relation_number=3):
        values = {
            "name": name,
            "sex": sex,
            "age": age,
            "grade": grade,
            "school_id": school_id,
            "class_id": class_id,
            "status": status,
            "relation_number": relation_number
        }
        student_obj = db_api.student_create(values)
        return student_obj

    def update(self, id="", **kwargs):
        if not id or not kwargs:
            return False
        _ = db_api.student_update(id, kwargs)
        return _

    def infos(self, id="", name="", grade="",
              school_id="", school_name="",
              class_id="", class_name="",
              relative_id="", relative_name="",
              limit=100, offset=1):
        offset = (offset - 1) * limit if offset > 0 else 0
        filters = dict()
        if id:
            filters.update({"id": id})
        if name:
            filters.update({"name": name})
        if grade:
            filters.update({"grade": grade})
        if school_id or school_name:
            if school_name:
                _school_list = db_api.school_list(name=school_name)
                if not _school_list:
                    return {"count": 0, "state": 0, "message": "query success", "data": []}
                school_id = _school_list[0].id
            filters.update({"school_id": school_id})

        if class_id or class_name:
            if class_name:
                _class_list = db_api.class_list(name=class_name)
                if not _class_list:
                    return {"count": 0, "state": 0, "message": "query success", "data": []}
                class_id = _class_list[0].id
            filters.update({"class_id": class_id})
        if relative_id or relative_name:
            if relative_name:
                _relative_list = db_api.relative_list(name=relative_name)
                if not _relative_list:
                    return {"count": 0, "state": 0, "message": "query success", "data": []}
                relative_id = _relative_list[0].id
            filters.update({"relative_id": relative_id})

        student_list = db_api.student_list(offset=offset, limit=limit, **filters)
        #关联学校和班级
        views_list = self.views(student_list)
        for view in views_list:
            school_list = db_api.school_list(id=view.get("school_id"))
            if school_list:
                view.update({"school_name": school_list[0].name})
            class_list = db_api.class_list(id=view.get("class_id"))
            if class_list:
                view.update({"class_name": class_list[0].name})
                view.update({"grade": class_list[0].grade})

        student_count = db_api.student_count(**filters)
        return {"count": student_count, "state": 0, "message": "query success", "data": views_list}