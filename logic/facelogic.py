#!/usr/bin/python
# -*- coding: utf-8 -*-

from db import api as db_api
from logic import Logic

class FaceLogic(Logic):
    def create_face(self, school_id, relevance_id, face_token, faceset_token, relevance_type=1):
        if not db_api.school_get(id=school_id):
            return

        if relevance_type == 1:
            _ = db_api.relative_get(id=relevance_id)
        if relevance_type == 2:
            _ = db_api.teacher_get(id=relevance_id)
        values = {
            "school_id": school_id,
            "relevance_id": relevance_id,
            "relevance_type": relevance_type,
            "face_token": face_token,
            "faceset_token": faceset_token
        }
        face_obj = db_api.face_create(values)
        return face_obj

    def infos(self, id="", relevance_id="", relevance_type=0, school_id="", face_token="",
              limit=100, offset=1):
        filters = {}
        if relevance_type!=0:
            filters.update({"relevance_type": relevance_type})
        if relevance_id:
            filters.update({"relevance_id": relevance_id})
        if school_id:
            filters.update({"school_id": school_id})
        if face_token:
            filters.update({"face_token": face_token})
        face_list = db_api.face_list(limit=2000, **filters)
        face_count = db_api.face_count(**filters)
        result = {"count": face_count, "state": 0, "message": "query success", "data": self.views(face_list)}
        return result

    def delete(self, id="", **kwargs):
        if not id:
            return "id is none"
        face_info = db_api.face_get(id=id)
        if not face_info:
            return "id not exit"
        if face_info.get("relevance_type") == 1:
            _relatve_info = db_api.relative_get(face_info.get("relevance_id"))
            if _relatve_info:
                return "exist relative"
        if face_info.get("relevance_type") == 2:
            _teacher_info = db_api.teacher_get(face_info.get("relevance_id"))
            if _teacher_info:
                return "exist teacher"
            
        _ = db_api.face_destroy(id)