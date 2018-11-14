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

    def infos(self, id="", relevance_id="", relevance_type=0, school_id="",
              limit=100, offset=1):
        filters = {}
        if relevance_type!=0:
            filters.update({"relevance_type": relevance_type})
        if relevance_id:
            filters.update({"relevance_id": relevance_id})
        if school_id:
            filters.update({"school_id": school_id})
        face_list = db_api.face_list(limit=2000, **filters)
        return self.views(face_list)

    def delete(self, id="", **kwargs):
        if not id:
            return
        _ = db_api.face_destroy(id)