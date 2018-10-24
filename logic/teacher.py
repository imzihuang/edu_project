#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import randint
import datetime
from util.convert import *
from db import api as db_api
from logic import Logic

class TeacherLogic(Logic):
    def __init__(self):
        super(TeacherLogic, self).__init__()

    def intput(self, name="", sex=0, age=0, school_id="", class_id="", phone=""):
        values = {
            "name": name,
            "sex": sex,
            "age": age,
            "school_id": school_id,
            "class_id": class_id,
            "phone": phone
        }
        teacher_obj = db_api.teacher_create(values)
        return teacher_obj

    def update(self, id="", **kwargs):
        if not id or not kwargs:
            return False
        _ = db_api.teacher_update(id, kwargs)
        return _

    def infos(self, id="", name="", school_id="", school_name="", class_id="", class_name="", phone="", limit=100, offset=1):
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

        if class_id or class_name:
            if class_name:
                _class_list = db_api.class_list(name=class_name)
                if not _class_list:
                    return {"count": 0, "state": 0, "message": "query success", "data": []}
                class_id = _class_list[0].id
            filters.update({"class_id": class_id})
        if phone:
            filters.update({"phone": phone})

        #关联班级名和学校名
        teacher_list = db_api.teacher_list(offset=offset, limit=limit, **filters)
        views_list = self.views(teacher_list)
        for view in views_list:
            school_list = db_api.school_list(id=view.get("school_id"))
            if school_list:
                view.update({"school_name": school_list[0].name})
            class_list = db_api.class_list(id=view.get("class_id"))
            if class_list:
                view.update({"class_name": class_list[0].name})
        teacher_count = db_api.teacher_count(**filters)
        return {"count": teacher_count, "state": 0, "message": "query success", "data": views_list}