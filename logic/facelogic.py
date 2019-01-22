#!/usr/bin/python
# -*- coding: utf-8 -*-

from db import api as db_api
from datetime import datetime
from logic import Logic
from util import exception
from util.face_recognition_api import face_recognition_yyl
import logging
LOG = logging.getLogger(__name__)

class FaceLogic(Logic):
    #def create_face(self, school_id, relevance_id, face_token, faceset_token, relevance_type=1):
    def input(self, school_id, phone, face_token, faceset_token, filename="", relevance_type=1, alias=""):
        if not db_api.school_get(id=school_id):
            return

        values = {
            "school_id": school_id,
            "phone": phone,
            "relevance_type": relevance_type,
            "face_token": face_token,
            "faceset_token": faceset_token,
            "img_path": filename,
            "alias": alias,
        }

        if relevance_type in (1, 3):
            relative_infos = db_api.relative_list(phone=phone)
            if not relative_infos:
                raise exception.NotFound(phone=phone)
            relative_ids = [relative_info.id for relative_info in relative_infos]
            relation_list = db_api.relation_list(relative_id=relative_ids)
            if relation_list:
                values.update({"student_id": relation_list[0].student_id})

        if relevance_type == 2:
            if not db_api.teacher_get_byphone(phone=phone):
                raise exception.NotFound(phone=phone)

        face_obj = db_api.face_create(values)
        return face_obj

    def infos(self, id="", phone="", relevance_type=0, limit=100, offset=1):
        filters = {}
        if id:
            filters.update({"id": id})

        if relevance_type != 0:
            filters.update({"relevance_type": relevance_type})
        if phone:
            filters.update({"phone": phone})
        face_list = db_api.face_list(limit=2000, **filters)
        face_count = db_api.face_count(**filters)
        view_list = self.views(face_list)
        for view in view_list:
            view.update({"img_path": "image/face/"+view.get("img_path", "")})
            _updated_time = datetime.strptime(view.get("updated_time"), "%Y-%m-%d %H:%M:%S")
            _now = datetime.now()
            if view.get("activate", True):
                if view.get("relevance_type", 1)==3 and (_now - _updated_time).seconds > 60:#60*60*24:
                    view.update({"activate": False})
        result = {"count": face_count, "state": 0, "message": "query success", "data": view_list}
        return result

    def delete(self, id="", **kwargs):
        if not id:
            return "id is none"
        face_info = db_api.face_get(id=id)
        if not face_info:
            return "id not exit"
        face_count = db_api.face_list(face_token=face_info.face_token)
        if face_count>1:
            _ = face_recognition_yyl.Face_Remove(face_info.school_id, face_info.face_token)
            LOG.info("remove facc:%r"%_)

        _ = db_api.face_destroy(id)

    def activate(self, id=""):
        LOG.info("activate id:%s"%id)
        if not id:
            return "id is none"
        face_info = db_api.face_get(id=id)
        if not face_info:
            return "id not exit"
        if face_info.relevance_type != 3:
            return "releance type error"
        db_api.face_update(id, {"activate": True})

    def disable(self, id=""):
        LOG.info("disable id:%s" % id)
        if not id:
            return "id is none"
        face_info = db_api.face_get(id=id)
        if not face_info:
            return "id not exit"
        if face_info.relevance_type != 3:
            return "releance type error"
        db_api.face_update(id, {"activate": False})

    def verify_authd(self, phone="", relevance_type=1):
        if relevance_type == 3:
            return False
        count = db_api.face_count(phone=phone)
        if count>0:
            return True
        return False

    def verify_face(self, face_token, school_id, cardcode):
        _face_list = db_api.face_list(face_token=face_token, school_id=school_id)
        if not _face_list:
            return None
        return self.views(_face_list)
        # for face_info in _face_list:
        #     relative_type = face_info.relevance_type
        #     #relevance_id = face_info.relevance_id
        #     if relative_type==2:
        #         # teacher
        #         return self.views(face_info)
        #     else:
        #         # relative
        #         return self.views(face_info)
        #return None


    def get_extra_face_count(self, phone=""):
        count = db_api.face_count(phone=phone, relevance_type=3)
        return count
