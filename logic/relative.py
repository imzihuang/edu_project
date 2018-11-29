#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import randint
import datetime
from util import convert
from db import api as db_api
from logic import Logic

import logging
from util import exception

LOG = logging.getLogger(__name__)

class RelativeLogic(Logic):
    def input(self, name="", sex=0, birthday="", phone="", describe=""):
        if birthday and not convert.is_date(birthday):
            raise exception.FormalError(birthday=birthday)
        if phone and not convert.is_mobile(phone):
            raise exception.FormalError(phone=phone)
        if not name:
            raise exception.ParamNone(name="")
        if phone and name:
            if db_api.relative_count(name=name, phone=phone)>0:
                raise exception.ParamExist(name=name, phone=phone)
        values = {
            "name": name,
            "sex": sex,
            "describe": describe
        }
        if phone:
            values.update({"phone": phone})
        if birthday:
            values.update({"birthday": birthday})
        relativel_obj = db_api.relative_create(values)
        return relativel_obj

    def update(self, id="", **kwargs):
        if not id or not kwargs:
            return False
        phone = convert.bs2utf8(kwargs.get("phone", ""))
        if phone and not convert.is_mobile(phone):
            raise exception.FormalError(phone=phone)
        _ = db_api.relative_update(id, kwargs)
        return _

    def infos(self, id="", name="",
              student_id="", student_name="",
              phone="",
              limit=100, offset=1):
        offset = (offset - 1) * limit if offset > 0 else 0
        filters = dict()
        if id:
            filters.update({"id": id})
        if name:
            filters.update({"name": name})

        if student_id or student_name:
            _relation_list = self._get_relations_by_student()
            if _relation_list:
                _ids = [_relation.relative_id for _relation in _relation_list]
                filters.update({"id": _ids})

        if phone:
            filters.update({"phone": phone})

        relative_list = db_api.relative_list(offset=offset, limit=limit, **filters)
        views_list = self.views(relative_list)

        relative_count = db_api.relative_count(**filters)
        return {"count": relative_count, "state": 0, "message": "query success", "data": views_list}

    def info(self, id):
        if not id:
            return
        relative_info = db_api.relative_get(id)
        return self.views(relative_info)

    def info_by_phone(self, phone=""):
        if not phone:
            return
        filters = dict()
        if phone:
            filters.update({"phone": phone})

        relative_infos = db_api.relative_list(**filters)
        if relative_infos:
            return self.views(relative_infos[0])

    def _get_relations_by_student(self, student_id="", student_name=""):
        if student_id:
            _relation_list = db_api.relation_list(student_id=student_id)
            return _relation_list

        _student_list = db_api.student_list(name=student_name)
        student_id = [_student.id for _student in _student_list]
        _relation_list = db_api.relation_list(student_id=student_id)
        return _relation_list

    def delete(self, id="", **kwargs):
        if not id:
            return "id is none"
        _relation_count = db_api.relation_count(relative_id=id)
        if _relation_count > 0:
            return "exist relation"
        db_api.relative_deleted(id=id)


