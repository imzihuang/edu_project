#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import randint
import datetime
from util.convert import *
from db import api as db_api
from logic import Logic

import logging
LOG = logging.getLogger(__name__)

class RelationLogic(Logic):

    def input(self, relation="", student_id="", relative_id=""):
        values = {
            "relation": relation,
            "student_id": student_id,
            "relative_id": relative_id
        }
        if not db_api.relative_get(relative_id):
            return
        if not db_api.student_get(student_id):
            return
        relation_obj = db_api.relation_create(values)
        return relation_obj

    def update(self, id="", **kwargs):
        if not id or not kwargs:
            return False
        _ = db_api.relation_update(id, kwargs)
        return _

    def infos(self, id="", student_id="", student_name="",
              relative_id="", relative_name="", phone="",
              class_id="", class_name="",
              grade_id="", grade_name="",
              limit=100, offset=1):
        offset = (offset - 1) * limit if offset > 0 else 0
        filters = dict()
        if id:
            filters.update({"id": id})
        if student_id or student_name:
            if not student_id:
                _student_list = db_api.student_list(name=student_name)
                if not _student_list:
                    return {"count": 0, "state": 0, "message": "query success", "data": []}
                student_id = [_student.id for _student in _student_list]
            filters.update({"student_id": student_id})

        if relative_id or relative_name or phone:
            if not relative_id:
                relative_filters = {}
                if relative_name:
                    relative_filters.update({"relative_name": relative_name})

                if phone:
                    relative_filters.update({"phone": phone})
                _relative_list = db_api.relative_list(**relative_filters)
                if not _relative_list:
                    return {"count": 0, "state": 0, "message": "query success", "data": []}
                relative_id = [_relative.id for _relative in _relative_list]
            filters.update({"relative_id": relative_id})

        if class_id or class_name:
            if not class_id:
                _class_list = db_api.class_list(name=class_name)
                if not _class_list:
                    return {"count": 0, "state": 0, "message": "query success", "data": []}
                class_id = [class_info.id for class_info in _class_list]
            filters.update({"class_id": class_id})

        if grade_id or grade_name:
            if not grade_id:
                _grade_list = db_api.grade_list(name=grade_name)
                if not _grade_list:
                    return {"count": 0, "state": 0, "message": "query success", "data": []}
                grade_id = [grade_info.id for grade_info in _grade_list]
            filters.update({"class_id": grade_id})

        relation_list = db_api.relation_list(offset=offset, limit=limit, **filters)
        # 管理学生信息和亲属信息
        views_list = self.views(relation_list)
        for view in views_list:
            _student_id = view.get("student_id")
            student_info = db_api.student_get(_student_id)
            view.update({"student_info": self.views(student_info)})

            _relative_id = view.get("relative_id")
            relative_info = db_api.relative_get(_relative_id)
            view.update({"relative_info": self.views(relative_info)})

        relation_count = db_api.relation_count(**filters)
        return {"count": relation_count, "state": 0, "message": "query success", "data": self.views(views_list)}

    def delete(self, id="", **kwargs):
        if not id:
            return
        db_api.relation_deleted(id=id)