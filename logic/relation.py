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

    def intput(self, relation="", student_id="", relative_id=""):
        values = {
            "relation": relation,
            "student_id": student_id,
            "relative_id": relative_id
        }
        relation_obj = db_api.relation_create(values)
        return relation_obj

    def update(self, id="", **kwargs):
        if not id or not kwargs:
            return False
        _ = db_api.relation_update(id, kwargs)
        return _

    def infos(self, id="", student_id="", relative_id="", limit=100, offset=1):
        offset = (offset - 1) * limit if offset > 0 else 0
        filters = dict()
        if id:
            filters.update({"id": id})
        if student_id:
            filters.update({"name": student_id})
        if relative_id:
            filters.update({"cardcode": relative_id})

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