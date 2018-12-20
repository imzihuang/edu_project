#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import randint
import datetime
from util.convert import *
from db import api as db_api
from logic import Logic
from util import exception

class ClassLogic(Logic):
    def input(self, name="", grade_id="", cardcode="", student_number=0):
        # verify school_id
        _ = db_api.grade_get(grade_id)
        if not _:
            raise exception.NotFound(grade_id=grade_id)
        _count = db_api.class_count(name=name)
        if _count>0:
            raise exception.ParamExist(name=name)
        values = {
            "name": name,
            "grade_id": grade_id,
            "cardcode": cardcode,
            "school_id": _.school_id,
            "student_number": student_number
        }
        class_obj = db_api.class_create(values)
        return class_obj

    def update(self, id="", **kwargs):
        if not id or not kwargs:
            raise exception.ParamNone(id=id)
        class_info = db_api.class_get(id)
        if not class_info:
            raise exception.NotFound(class_id=id)
        if kwargs.get("grade_id", ""):
            _ = db_api.grade_get(kwargs.get("grade_id", ""))
            if not _:
                raise exception.NotFound(grade_id=kwargs.get("grade_id", ""))
            kwargs.update({"school_id": _.school_id})

        name = kwargs.get("name", "")
        if name and class_info.name != name and db_api.class_list(name=name):
            raise exception.ParamExist(class_name=name)

        _ = db_api.class_update(id, kwargs)
        return _

    def infos(self, id="", name="",
              school_id="", school_name="",
              grade_id="", grade_name="",
              cardcode="", limit=100, offset=1):
        offset = (offset - 1) * limit if offset > 0 else 0
        filters = dict()
        if id:
            filters.update({"id": id})
        if name:
            filters.update({"name": name})
        if cardcode:
            filters.update({"cardcode": cardcode})
        if school_id or school_name:
            if not school_id:
                _school_list = db_api.school_list(name=school_name)
                if not _school_list:
                    return {"count": 0, "state": 0, "message": "query success", "data": []}
                school_id = [school_info.id for school_info in _school_list]
            filters.update({"school_id": school_id})

        if grade_id or grade_name:
            if not grade_id:
                _grade_list = db_api.grade_list(name=grade_name)
                if not _grade_list:
                    return
                grade_id = [grade_info.id for grade_info in _grade_list]
            filters.update({"grade_id": grade_id})

        class_list = db_api.class_list(offset=offset, limit=limit, **filters)
        #更新学生数和学校名称
        views_list = self.views(class_list)
        for view in views_list:
            school_info = db_api.school_get(id=view.get("school_id", ""))
            if school_info:
                view.update({"school_name": school_info.name})
            grade_info = db_api.grade_get(id=view.get("grade_id", ""))
            if grade_info:
                view.update({"grade_name": grade_info.name})
            student_count = db_api.student_count(class_id=view.get("id"))
            view.update({"reality_number": student_count})

        class_count = db_api.class_count(**filters)
        return {"count": class_count, "state": 0, "message": "query success", "data": views_list}

    def delete(self, id="", **kwargs):
        if not id:
            return "id is none"
        relevance_student_count = db_api.student_count(class_id=id)
        if relevance_student_count > 0:
            return "exist student"
        relevance_teacher_count = db_api.teacher_count(class_id=id)
        if relevance_teacher_count > 0:
            return "exist teacher"
        db_api.class_deleted(id=id)
