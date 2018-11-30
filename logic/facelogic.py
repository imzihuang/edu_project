#!/usr/bin/python
# -*- coding: utf-8 -*-

from db import api as db_api
from datetime import datetime
from logic import Logic
from util import exception

class FaceLogic(Logic):
    #def create_face(self, school_id, relevance_id, face_token, faceset_token, relevance_type=1):
    def input(self, school_id, relevance_id, face_token, faceset_token, filename="", relevance_type=1, alias=""):
        if not db_api.school_get(id=school_id):
            return

        values = {
            "school_id": school_id,
            "relevance_id": relevance_id,
            "relevance_type": relevance_type,
            "face_token": face_token,
            "faceset_token": faceset_token,
            "img_path": filename,
            "alias": alias,
        }

        if relevance_type in (1, 3):
            relation_list = db_api.relation_list(relative_id=relevance_id)
            if not db_api.relative_get(id=relevance_id) or not relation_list:
                raise exception.NotFound(code=relevance_id)

            values.update({"student_id": relation_list[0].student_id})

        if relevance_type == 2:
            if not db_api.teacher_get(id=relevance_id):
                raise exception.NotFound(code=relevance_id)

        face_obj = db_api.face_create(values)
        return face_obj

    def infos(self, id="", relevance_id="", relevance_type=0, limit=100, offset=1):
        filters = {}
        if relevance_type != 0:
            filters.update({"relevance_type": relevance_type})
        if relevance_id:
            filters.update({"relevance_id": relevance_id})
        face_list = db_api.face_list(limit=2000, **filters)
        face_count = db_api.face_count(**filters)
        view_list = self.views(face_list)
        for view in view_list:
            view.update({"img_path": "image/face/"+view.get("img_path", "")})
            _updated_time = datetime.strptime(view.get("updated_time"), "%Y-%m-%d %H:%M:%S")
            _now = datetime.now()
            if view.get("relevance_type", 1)==3 and (_now - _updated_time).seconds > 60:#60*60*24:
                view.update({"activate": False})
            else:
                view.update({"activate": True})
        result = {"count": face_count, "state": 0, "message": "query success", "data": view_list}
        return result

    def delete(self, id="", **kwargs):
        if not id:
            return "id is none"
        face_info = db_api.face_get(id=id)
        if not face_info:
            return "id not exit"
        if face_info.relevance_type == 1:
            _relatve_info = db_api.relative_get(face_info.get("relevance_id"))
            if _relatve_info:
                return "exist relative"
        if face_info.relevance_type == 2:
            _teacher_info = db_api.teacher_get(face_info.get("relevance_id"))
            if _teacher_info:
                return "exist teacher"

        _ = db_api.face_destroy(id)

    def active(self, id=""):
        if not id:
            return "id is none"
        face_info = db_api.face_get(id=id)
        if not face_info:
            return "id not exit"
        if face_info.relevance_type != 3:
            return "releance type error"
        db_api.face_update(id, {"deleted": False})

    def verify_authd(self, relevance_id="", relevance_type=1):
        if relevance_type == 3:
            return False
        count = db_api.face_count(relevance_id=relevance_id, relevance_type=relevance_type)
        if count>0:
            return True
        return False

    def get_extra_face_count(self, relevance_id=""):
        count = db_api.face_count(relevance_id=relevance_id, relevance_type=3)
        return count