#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import randint
from util import convert
from datetime import datetime, date, timedelta
from db import api as db_api
from db import combination as db_combination
from logic import Logic
from util import exception
import logging
LOG = logging.getLogger(__name__)

class StudentLogic(Logic):
    def __init__(self):
        pass

    def input(self, name="", sex=0, birthday="", class_id="", status="apply", relation_number=3, describe=""):
        if birthday and not convert.is_date(birthday):
            raise exception.FormalError(birthday=birthday)
        if not name:
            raise exception.ParamNone(name="")
        if not class_id:
            raise exception.ParamNone(name="")
        class_info = db_api.class_get(id=class_id)
        if not class_info:
            raise exception.NotFound(code=class_id)
        values = {
            "name": name,
            "sex": sex,
            #"birthday": birthday,
            "school_id": class_info.school_id,
            "grade_id": class_info.grade_id,
            "class_id": class_id,
            "describe": describe,
            #"status": status,
            "relation_number": relation_number
        }
        if birthday:
            values.update({"birthday": birthday})
        student_obj = db_api.student_create(values)
        if student_obj:
            history_values={
                "student_id": student_obj.get("id"),
                "staus": status
            }
            db_api.student_history_create(history_values)
        student_obj.update({"status": status})
        return student_obj

    def update(self, id="", **kwargs):
        if not id or not kwargs:
            raise exception.ParamNone(id=id)
        if kwargs.get("class_id"):
            class_info = db_api.class_get(id=kwargs.get("class_id"))
            kwargs.update({
                "school_id": class_info.school_id,
                "grade_id": class_info.grade_id,
            })
        status = kwargs.pop("status", "")
        _ = db_api.student_update(id, kwargs)
        if status:
            history_values = {
                "student_id": id,
                "staus": status
            }
            db_api.student_history_create(history_values)
        return _

    def infos(self, id="", name="",
              school_id="", school_name="",
              grade_id="", grade_name="",
              class_id="", class_name="",
              relative_id="", relative_name="",
              limit=100, offset=1):
        offset = (offset - 1) * limit if offset > 0 else 0
        filters = dict()
        if id:
            filters.update({"id": id})
        if name:
            filters.update({"name": name})
        if school_id or school_name:
            if not school_id:
                _school_list = db_api.school_list(name=school_name)
                if not _school_list:
                    return {"count": 0, "state": 0, "message": "query success", "data": []}
                school_id = [school_info.id for school_info in _school_list]
            filters.update({"school_id": school_id})

        if grade_id or grade_name:
            if not grade_id:
                _grade_list = db_api.grade_list(name=grade_name)
                if not _grade_list:
                    return {"count": 0, "state": 0, "message": "query success", "data": []}
                grade_id = [grade_info.id for grade_info in _grade_list]
            filters.update({"grade_id": grade_id})

        if class_id or class_name:
            if not class_id:
                _class_list = db_api.class_list(name=class_name)
                if not _class_list:
                    return {"count": 0, "state": 0, "message": "query success", "data": []}
                class_id = [class_info.id for class_info in _class_list]
            filters.update({"class_id": class_id})

        if relative_id or relative_name:
            _relation_list = self._get_relations_by_relative(relative_id, relative_name)
            if _relation_list:
                _ids = [_relation.student_id for _relation in _relation_list]
                filters.update({"id": _ids})

        student_list = db_api.student_list(offset=offset, limit=limit, **filters)
        #关联学校和班级
        views_list = self.views(student_list)
        for view in views_list:
            school_info = db_api.school_get(id=view.get("school_id"))
            if school_info:
                view.update({"school_name": school_info.name})
            grade_info = view.get("grade_info", None)
            if grade_info:
                view.update({"grade_name": grade_info.get("name")})
            class_info = view.get("class_info", None)
            if class_info:
                view.update({"class_name": class_info.get("name")})
            relation_list = self._get_relations_by_student(view.get("id"))
            if relation_list:
                view.update({"relation_list": relation_list})

        student_count = db_api.student_count(**filters)
        return {"count": student_count, "state": 0, "message": "query success", "data": views_list}

    def infos_for_sign_month(self, id="", name="",
                       school_id="",
                       grade_id="", class_id="",
                       relative_id="", sign_date="",
                       limit=100, offset=1):
        offset = (offset - 1) * limit if offset > 0 else 0
        filters = dict()
        if id:
            filters.update({"id": id})
        if name:
            filters.update({"name": name})
        if school_id:
            filters.update({"school_id": school_id})
        if grade_id:
            filters.update({"grade_id": grade_id})
        if class_id:
            filters.update({"class_id": class_id})
        if relative_id:
            _relation_list = self._get_relations_by_relative(relative_id)
            if _relation_list:
                _ids = [_relation.student_id for _relation in _relation_list]
                filters.update({"id": _ids})

        student_list = db_api.student_list(offset=offset, limit=limit, **filters)
        student_count = db_api.student_count(**filters)

        # 关联学校和班级，还有学生得签到（学生亲属的签到信息）
        views_list = self.views(student_list)
        for view in views_list:
            school_info = db_api.school_get(id=view.get("school_id"))
            if school_info:
                view.update({"school_name": school_info.name})
            grade_info = view.get("grade_info", None)
            if grade_info:
                view.update({"grade_name": grade_info.get("name")})
            class_info = view.get("class_info", None)
            if class_info:
                view.update({"class_name": class_info.get("name")})

            sign_count, late_count, early_count, sign_date = self.com_sign(view.get("id"), sign_date)
            view.update({"sign": sign_count,
                         "late": late_count,
                         "early": early_count,
                         "sign_date": datetime.strftime(sign_date, "%Y-%m")})

        return {"count": student_count, "state": 0, "message": "query success", "data": views_list}

    def infos_for_sign_day(self, id="", name="",
                       school_id="",
                       grade_id="", class_id="",
                       relative_id="", sign_date="",
                       limit=100, offset=1):
        offset = (offset - 1) * limit if offset > 0 else 0
        filters = dict()
        if id:
            filters.update({"id": id})
        if name:
            filters.update({"name": name})
        if school_id:
            filters.update({"school_id": school_id})
        if grade_id:
            filters.update({"grade_id": grade_id})
        if class_id:
            filters.update({"class_id": class_id})
        if relative_id:
            _relation_list = self._get_relations_by_relative(relative_id)
            if _relation_list:
                _ids = [_relation.student_id for _relation in _relation_list]
                filters.update({"id": _ids})

        student_list = db_api.student_list(offset=offset, limit=limit, **filters)
        student_count = db_api.student_count(**filters)

        # 关联学校和班级，还有学生得签到（学生亲属的签到信息）
        views_list = self.views(student_list)
        for view in views_list:
            school_info = db_api.school_get(id=view.get("school_id"))
            if school_info:
                view.update({"school_name": school_info.name})
            grade_info = view.get("grade_info", None)
            if grade_info:
                view.update({"grade_name": grade_info.get("name")})
            class_info = view.get("class_info", None)
            if class_info:
                view.update({"class_name": class_info.get("name")})

            sign_date = datetime.strptime(sign_date, "%Y-%m-%d") if convert.is_date(sign_date) else date.today()
            sign_status_list = db_api.student_sign_status_list(sign_date, sign_date, student_id=view.get("id"))
            if sign_status_list:
                view.update({
                    "sign_date": datetime.strftime(sign_date, "%Y-%m-%d"),
                    "morning": sign_status_list[0].morning if sign_status_list[0].morning else "",
                    "afternoon": sign_status_list[0].afternoon if sign_status_list[0].afternoon else ""
                })

        return {"count": student_count, "state": 0, "message": "query success", "data": views_list}


    def info_detail_for_sign(self, id="", start_date="", end_date=""):
        if not id:
            raise exception.ParamNone(id=id)
        student_info = db_api.student_get(id)
        if not student_info:
            raise exception.NotFound(id=id)

        LOG.info("student_id%s"%id)
        # 关联学校和班级，还有学生得签到（学生亲属的签到信息）
        student_info = self.views(student_info)
        sign_detail = self.com_sign_detail(id, start_date, end_date)
        sign_data = []
        for sign_status in sign_detail:
            sign_data.append({
                "date": datetime.strftime(sign_status.sign_date, "%Y-%m-%d"),
                "status": sign_status.status,
                "morning": sign_status.morning if sign_status.morning else "",
                "afternoon": sign_status.afternoon if sign_status.afternoon else ""
            })
            #result.update({datetime.strftime(sign_status.sign_date, "%Y-%m-%d"): sign_status.status})

        student_info.update({"sign_data": sign_data})
        return student_info



    def _get_relations_by_relative(self, relative_id="", relative_name=""):
        if relative_id:
            _relation_list = db_api.relation_list(relative_id=relative_id)
            return _relation_list

        _relative_list = db_api.relative_list(name=relative_name)
        relative_id = [_relative.id for _relative in _relative_list]
        _relation_list = db_api.relation_list(relative_id=relative_id)
        return _relation_list

    def _get_relations_by_student(self, student_id=""):
        relation_list = db_api.relation_list(student_id=student_id)
        relation_list = self.views(relation_list)
        if not relation_list:
            return
        for relavtion in relation_list:
            relative_info = db_api.relative_get(relavtion.get("relative_id"))
            relavtion.update({"relation_info": self.views(relative_info)})

        return relation_list

    def _get_relative_by_student(self, student_id=""):
        relation_list = db_api.relation_list(student_id=student_id)
        relation_list = self.views(relation_list)
        if not relation_list:
            return
        for relavtion in relation_list:
            relative_info = db_api.relative_get(relavtion.get("relative_id"))
            relavtion.update({
                "phone": relative_info.phone,
                "name": relative_info.name,
                "sex": relative_info.sex,
                "birthday": relative_info.birthday,
            })

        return relation_list


    def delete(self, id="", **kwargs):
        if not id:
            return "id is none"
        _relation_count = db_api.relation_count(student_id=id)
        if _relation_count > 0:
            return "exist relation"

        db_api.student_deleted(id=id)

        history_values={
            "student_id": id,
            "status": "deleted"
        }
        db_api.student_history_create(history_values)

    def combination_delete(self, id=""):
        if not id:
            return "id is none"
        db_combination.delete_student(student_id=id)
        history_values = {
            "student_id": id,
            "status": "deleted"
        }
        db_api.student_history_create(history_values)

    def com_sign(self, student_id, sign_date=""):
        """
        统计亲属签到信息
        :param student_id: 学生编号
        :return:
        """
        sign_date = datetime.strptime(sign_date, "%Y-%m-%d") if convert.is_date(sign_date) else datetime.now()
        firstDay, lastDay = convert.getMonthFirstDayAndLastDay(sign_date.year, sign_date.month)
        sign_count = 0  # 出勤
        late_count = 0  # 早上迟到
        early_count = 0  # 下午早退

        sign_status_list = db_api.student_sign_status_list(firstDay, lastDay, student_id=student_id)
        for status_info in sign_status_list:
            if status_info.status == "11":
                sign_count += 1
            if status_info.status[0] == "2":
                late_count += 1
            if status_info.status[1] == "2":
                early_count += 1
        return sign_count, late_count, early_count, sign_date

    def com_sign_detail(self, student_id, start_date="", end_date=""):
        """

        :param relation_list:
        :param start_date:
        :param end_date:
        :return: {"2018-12-01": "11"}
        """
        if not convert.is_date(start_date) or not convert.is_date(end_date):
            start_date, end_date = convert.getMonthFirstDayAndLastDay(datetime.now().year, datetime.now().month)
        else:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            start_date = date(start_date.year, start_date.month, start_date.day)
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
            end_date = date(end_date.year, end_date.month, end_date.day)
        LOG.info("sign start end:%r, %r"%(start_date, end_date))
        #result={}
        sign_status_list = db_api.student_sign_status_list(start_date, end_date, student_id=student_id)
        # for sign_status in sign_status_list:
        #     result.update({datetime.strftime(sign_status.sign_date, "%Y-%m-%d"): sign_status.status})

        return sign_status_list

    def student_relative_excel(self, student_id="", student_name="", school_id="", grade_id="", class_id=""):
        filters = {}
        if student_id:
            filters.update({"id": student_id})
        if student_name:
            filters.update({"name": student_name})
        if school_id:
            filters.update({"school_id": school_id})
        if grade_id:
            filters.update({"grade_id": grade_id})
        if class_id:
            filters.update({"grade_id": class_id})

        student_list = db_api.student_list(**filters)
        views_list = self.views(student_list)
        for view in views_list:
            school_info = db_api.school_get(id=view.get("school_id"))
            if school_info:
                view.update({"school_name": school_info.name})
            grade_info = view.get("grade_info", None)
            if grade_info:
                view.update({"grade_name": grade_info.get("name")})
            class_info = view.get("class_info", None)
            if class_info:
                view.update({"class_name": class_info.get("name")})
            relation_list = self._get_relative_by_student(view.get("id"))
            if relation_list:
                view.update({"relative_list": relation_list})
        return views_list

