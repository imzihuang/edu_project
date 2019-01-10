#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import randint
import datetime
from util import convert
from util import exception
from db import api as db_api
from logic import Logic

class GradeLogic(Logic):
    def input(self, name="", school_id=""):
        # verify school_id
        if not db_api.school_get(school_id):
            raise exception.NotFound(school_id=school_id)
        _count = db_api.class_count(name=name)
        if _count > 0:
            raise exception.ParamExist(name=name)
        values = {
            "name": name,
            "school_id": school_id,
        }
        grade_obj = db_api.grade_create(values)
        return grade_obj

    def update(self, id="", **kwargs):
        if not id or not kwargs:
            raise exception.ParamNone(grade_id=id)
        garde_info = db_api.grade_get(id)
        if not garde_info:
            raise exception.NotFound(grade_id=id)

        if kwargs.get("school_id", ""):
            _ = db_api.school_get(kwargs.get("school_id", ""))
            if not _:
                raise exception.NotFound(school_id=kwargs.get("school_id", ""))

        name = kwargs.get("name", "")
        if name and convert.bs2utf8(garde_info.name) != name and db_api.teacher_list(name=name):
            raise exception.ParamExist(grade_name=name)

        _ = db_api.grade_update(id, kwargs)
        return _

    def infos(self, id="", name="", school_id="", school_name="", limit=100, offset=1):
        offset = (offset - 1) * limit if offset > 0 else 0
        filters = dict()
        if id:
            filters.update({"id": id})
        if name:
            filters.update({"name": name})
        if school_id or school_name:
            if not school_id:
                _school_list = db_api.school_list(name=school_name)
                if not _school_list:
                    return {"count": 0, "state": 0, "message": "query success", "data": []}
                school_id = _school_list[0].id
            filters.update({"school_id": school_id})

        grade_list = db_api.grade_list(offset=offset, limit=limit, **filters)
        #更新学生数和学校名称
        views_list = self.views(grade_list)
        for view in views_list:
            school_list = db_api.school_list(id=view.get("school_id"))
            if school_list:
                view.update({"school_name": school_list[0].name})

        grade_count = db_api.grade_count(**filters)
        return {"count": grade_count, "state": 0, "message": "query success", "data": views_list}

    def delete(self, id="", **kwargs):
        if not id:
            return "id is none"
        relevance_class_count = db_api.class_count(grade_id=id)
        if relevance_class_count>0:
            return "exist class"
        db_api.grade_deleted(id=id)