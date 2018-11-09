#!/usr/bin/python
# -*- coding: utf-8 -*-

from db import api as db_api
from logic import Logic

class FaceLogic(Logic):
    def create_face(self, school_id, relative_id, face_token, faceset_token):
        _ = db_api.school_get(id=school_id)
        _ = db_api.relative_get(id=relative_id)
        values = {
            "school_id": school_id,
            "relative_id": relative_id,
            "face_token": face_token,
            "faceset_token": faceset_token
        }
        face_obj = db_api.face_create(values)
        return face_obj

    def infos(self, id="", relative_id="", school_id="",
              limit=100, offset=1):
        filters = {}
        if relative_id:
            filters.update({"relative_id": relative_id})
        if school_id:
            filters.update({"school_id": school_id})
        face_list = db_api.face_list(limit=2000, **filters)
        return self.views(face_list)

    def delete(self, id=""):
        if not id:
            return
        _ = db_api.face_destroy(id)