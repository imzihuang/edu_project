#!/usr/bin/python
# -*- coding: utf-8 -*-

from db import api as db_api
from logic import Logic
import logging

LOG = logging.getLogger(__name__)

class Teacher_HistoryLogic(Logic):
    def intput(self, teacher_id, status, describe=""):
        if not teacher_id or not status:
            LOG.error("student_id name or status is None")
            return
        db_api.teacher_get(id=teacher_id)
        values = {
            "teacher_id": teacher_id,
            "status": status,
            "describe": describe
        }
        _ = db_api.teacher_history_create(values)
        return values

    def update(self, id="", **kwargs):
        pass

    def infos(self, id="", teacher_id="", teacher_name="", status="", limit=100, offset=1):
        offset = (offset-1)*limit if offset > 0 else 0
        filters = dict()
        if id:
            filters.update({"id": id})
        if teacher_id or teacher_name:
            if not teacher_id:
                _teacher_list = db_api.teacher_list(name=teacher_name)
                if _teacher_list:
                    teacher_id = [teacher_info.id for teacher_info in _teacher_list]
            filters.update({"teacher_id": teacher_id})
        if status:
            filters.update({"status": status})

        history_list = db_api.teacher_history_list(offset=offset, limit=limit, **filters)
        views_list = self.views(history_list)
        for view in views_list:
            teacher_info = db_api.teacher_get(id=view.get("teacher_id"))
            if teacher_info:
                view.update({"teacher_name": teacher_info.name})
        history_count = db_api.teacher_history_count(**filters)
        return {"count": history_count, "state": 0, "message": "query success", "data": views_list}
