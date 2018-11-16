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

    def input(self, name="", sex=0, birthday="",
              school_id="", class_id="",
              phone="", position=2, describe="", status="education"):
        if birthday and not is_date(birthday):
            raise exception.FormalError(birthday=birthday)
        if not name or not class_id:
            raise exception.ParamNone(class_id="")
        class_info = None
        if class_id:
            class_id = class_id.split(",")
            class_list = db_api.class_list(id=class_id)
            class_info = class_list[0]

        values = {
            "name": name,
            "sex": sex,
            #"birthday": birthday,
            #"school_id": class_info.school_id,
            #"grade_id": class_info.grade_id,
            "class_id": class_id,
            "phone": phone,
            "describe": describe
        }
        if class_info:
            if class_info.school_id != school_id:
                raise exception.ParamNone(school_id=school_id)
            values.update({"school_id": school_id,
                            "grade_id": class_info.grade_id,
                           })
        if birthday:
            values.update({"birthday": birthday})
        if position != 0:
            values.update({"position": position})
        teacher_obj = db_api.teacher_create(values)

        if teacher_obj:
            history_values = {
                "teacher_id": teacher_obj.get("id"),
                "staus": status
            }
            db_api.teacher_history_create(history_values)
            teacher_obj.update({"status": status})
        return teacher_obj

    def update(self, id="", **kwargs):
        if not id or not kwargs:
            return False
        if kwargs.get("class_id"):
            class_id = kwargs.get("class_id").split(",")
            class_list = db_api.class_list(id=class_id)
            kwargs.update({
                "school_id": class_list[0].school_id,
                "grade_id": class_list[0].grade_id,
            })

        _ = db_api.teacher_update(id, kwargs)
        return _

    def infos(self, id="", name="",
              school_id="", school_name="",
              grade_id="", grade_name="",
              class_id="", class_name="",
              phone="", position=0,
              limit=100, offset=1):
        offset = (offset - 1) * limit if offset > 0 else 0
        filters = dict()
        if id:
            filters.update({"id": id})
        if name:
            filters.update({"name": name})
        if position in (1, 2):
            filters.update({"position": position})
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

            class_id = view.get("class_id")("class_id").split(",")
            class_list = db_api.class_list(id=class_id)
            if class_list:
                view.update({"class_info": self.views(class_list)})
        teacher_count = db_api.teacher_count(**filters)
        return {"count": teacher_count, "state": 0, "message": "query success", "data": views_list}

    def delete(self, id="", **kwargs):
        if not id:
            return
        db_api.teacher_deleted(id=id)