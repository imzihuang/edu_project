#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import randint
import datetime
from util.convert import *
from db import api as db_api
from logic import Logic
from util import exception

class StudentLogic(Logic):
    def __init__(self):
        pass

    def input(self, name="", sex=0, birthday="", class_id="", status="apply", relation_number=3, describe=""):
        if birthday and not is_date(birthday):
            raise exception.FormalError(birthday=birthday)
        if not name:
            raise exception.ParamNone(name="")
        if not class_id:
            raise exception.ParamNone(name="")
        class_info = db_api.class_get(id=class_id)
        if not class_info:
            raise exception.NotFound(code=class_id)
        values = {
            "name": name,
            "sex": sex,
            #"birthday": birthday,
            "school_id": class_info.school_id,
            "grade_id": class_info.grade_id,
            "class_id": class_id,
            "describe": describe,
            #"status": status,
            "relation_number": relation_number
        }
        if birthday:
            values.update({"birthday": birthday})
        student_obj = db_api.student_create(values)
        if student_obj:
            history_values={
                "student_id": student_obj.get("id"),
                "staus": status
            }
            db_api.student_history_create(history_values)
        student_obj.update({"status": status})
        return student_obj

    def update(self, id="", **kwargs):
        if not id or not kwargs:
            return False
        if kwargs.get("class_id"):
            class_info = db_api.class_get(id=kwargs.get("class_id"))
            kwargs.update({
                "school_id": class_info.school_id,
                "grade_id": class_info.grade_id,
            })
        _ = db_api.student_update(id, kwargs)
        return _

    def infos(self, id="", name="",
              school_id="", school_name="",
              grade_id="", grade_name="",
              class_id="", class_name="",
              relative_id="", relative_name="",
              limit=100, offset=1):
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
                school_id = [school_info.id for school_info in _school_list]
            filters.update({"school_id": school_id})

        if grade_id or grade_name:
            if not grade_id:
                _grade_list = db_api.grade_list(name=grade_name)
                if not _grade_list:
                    return {"count": 0, "state": 0, "message": "query success", "data": []}
                grade_id = [grade_info.id for grade_info in _grade_list]
            filters.update({"grade_id": grade_id})

        if class_id or class_name:
            if not class_id:
                _class_list = db_api.class_list(name=class_name)
                if not _class_list:
                    return {"count": 0, "state": 0, "message": "query success", "data": []}
                class_id = [class_info.id for class_info in _class_list]
            filters.update({"class_id": class_id})

        if relative_id or relative_name:
            _relation_list = self._get_relations_by_relative(relative_id, relative_name)
            if _relation_list:
                _ids = [_relation.student_id for _relation in _relation_list]
                filters.update({"id": _ids})

        student_list = db_api.student_list(offset=offset, limit=limit, **filters)
        #关联学校和班级
        views_list = self.views(student_list)
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

        student_count = db_api.student_count(**filters)
        return {"count": student_count, "state": 0, "message": "query success", "data": views_list}

    def _get_relations_by_relative(self, relative_id="", relative_name=""):
        if relative_id:
            _relation_list = db_api.relation_list(relative_id=relative_id)
            return _relation_list

        _relative_list = db_api.relative_list(name=relative_name)
        relative_id = [_relative.id for _relative in _relative_list]
        _relation_list = db_api.relation_list(relative_id=relative_id)
        return _relation_list

    def delete(self, id="", **kwargs):
        if not id:
            return
        db_api.student_deleted(id=id)