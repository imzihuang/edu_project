#!/usr/bin/python
# -*- coding: utf-8 -*-

from db import api as db_api
from logic import Logic
import logging

LOG = logging.getLogger(__name__)

class Student_HistoryLogic(Logic):
    def intput(self, student_id, status, describe=""):
        if not student_id or not status:
            LOG.error("student_id name or status is None")
            return
        db_api.student_get(id=student_id)
        values = {
            "student_id": student_id,
            "status": status,
            "describe": describe
        }
        _ = db_api.student_history_create(values)
        return values

    def update(self, id="", **kwargs):
        pass

    def infos(self, id="", student_id="", student_name="", status="", limit=100, offset=1):
        offset = (offset-1)*limit if offset > 0 else 0
        filters = dict()
        if id:
            filters.update({"id": id})
        if student_id or student_name:
            if student_name:
                _student_list = db_api.student_list(name=student_name)
                if _student_list:
                    student_id = [student_info.id for student_info in _student_list]
            filters.update({"student_id": student_id})
        if status:
            filters.update({"status": status})

        history_list = db_api.student_history_list(offset=offset, limit=limit, **filters)
        views_list = self.views(history_list)
        for view in views_list:
            student_info = db_api.student_get(id=view.get("student_id"))
            if student_info:
                view.update({"student_name": student_info.name})
        history_count = db_api.student_history_count(**filters)
        return {"count": history_count, "state": 0, "message": "query success", "data": views_list}
