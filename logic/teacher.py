#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import randint
import datetime
from util.convert import *
from db import api as db_api
from logic import Logic
from util import exception

class TeacherLogic(Logic):
    def __init__(self):
        super(TeacherLogic, self).__init__()

    def intput(self, name="", sex=0, birthday="", class_id="", phone=""):
        if not is_date(birthday):
            raise exception.FormalError(birthday=birthday)
        if not name or not class_id:
            raise exception.ParamNone(class_id="")
        class_info = db_api.class_get(id=class_id)
        values = {
            "name": name,
            "sex": sex,
            "birthday": birthday,
            "school_id": class_info.school_id,
            "grade_id": class_info.grade_id,
            "class_id": class_id,
            "phone": phone
        }
        teacher_obj = db_api.teacher_create(values)
        return teacher_obj

    def update(self, id="", **kwargs):
        if not id or not kwargs:
            return False
        if kwargs.get("class_id"):
            class_info = db_api.class_get(id=kwargs.get("class_id"))
            kwargs.update({
                "school_id": class_info.school_id,
                "grade_id": class_info.grade_id,
            })

        _ = db_api.teacher_update(id, kwargs)
        return _

    def infos(self, id="", name="",
              school_id="", school_name="",
              grade_id="", grade_name="",
              class_id="", class_name="",
              phone="", limit=100, offset=1):
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
                school_id = [school_info.id for school_info in _school_list]
            filters.update({"school_id": school_id})

        if grade_id or grade_name:
            if grade_name:
                _grade_list = db_api.grade_list(name=grade_name)
                if not _grade_list:
                    return {"count": 0, "state": 0, "message": "query success", "data": []}
                grade_id = [grade_info.id for grade_info in _grade_list]
            filters.update({"grade_id": grade_id})

        if class_id or class_name:
            if class_name:
                _class_list = db_api.class_list(name=class_name)
                if not _class_list:
                    return {"count": 0, "state": 0, "message": "query success", "data": []}
                class_id = [class_info.id for class_info in _class_list]
            filters.update({"class_id": class_id})
        if phone:
            filters.update({"phone": phone})

        #关联班级名和学校名
        teacher_list = db_api.teacher_list(offset=offset, limit=limit, **filters)
        views_list = self.views(teacher_list)
        for view in views_list:
            school_info = db_api.school_get(id=view.get("school_id"))
            if school_info:
                view.update({"school_name": school_info.name})
            grade_info = db_api.grade_get(id=view.get("grade_id"))
            if grade_info:
                view.update({"grade_name": grade_info.name})
            class_info = db_api.class_get(id=view.get("class_id"))
            if class_info:
                view.update({"class_name": class_info.name})
        teacher_count = db_api.teacher_count(**filters)
        return {"count": teacher_count, "state": 0, "message": "query success", "data": views_list}

    def delete(self, id="", **kwargs):
        if not id:
            return
        db_api.teacher_deleted(id=id)