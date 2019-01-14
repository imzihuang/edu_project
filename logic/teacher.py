#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import randint
import datetime
from util import convert
from db import api as db_api
from logic import Logic
from util import exception

class TeacherLogic(Logic):
    def __init__(self):
        super(TeacherLogic, self).__init__()

    def input(self, name="", sex=0, birthday="",
              school_id="", class_id="",
              phone="", position=2, describe="", status="education"):
        if birthday and not convert.is_date(birthday):
            raise exception.FormalError(birthday=birthday)
        if not name:
            raise exception.ParamNone(name="")
        if phone:
            _count = db_api.teacher_count(phone=phone)
            if _count>0:
                raise exception.ParamExist(phone=phone)
        values = {
            "name": name,
            "sex": sex,
            #"birthday": birthday,
            "school_id": school_id,
            "phone": phone,
            "describe": describe,
            "status": status
        }
        if class_id:
            class_info = db_api.class_get(id=class_id)
            if class_info:
                values.update({"school_id": class_info.school_id,
                               "grade_id": class_info.grade_id,
                               "class_id": class_id,
                               })
        if birthday:
            values.update({"birthday": birthday})
        if position != 0:
            values.update({"position": position})
        teacher_obj = db_api.teacher_create(values)

        if teacher_obj:
            history_values = {
                "teacher_id": teacher_obj.get("id"),
                "status": status
            }
            db_api.teacher_history_create(history_values)
            #teacher_obj.update({"status": status})
        return teacher_obj

    def update(self, id="", **kwargs):
        if not id or not kwargs:
            raise exception.ParamNone(id=id)
        teacher_info = db_api.teacher_get(id)
        if not teacher_info:
            raise exception.NotFound(id=id)
        if kwargs.get("class_id", ""):
            class_info = db_api.class_get(id=kwargs.get("class_id"))
            if not class_info:
                raise exception.NotFound(class_id=kwargs.get("class_id", ""))
            kwargs.update({
                "school_id": class_info.school_id,
                "grade_id": class_info.grade_id,
            })
        name=kwargs.get("name", "")
        if name and convert.bs2utf8(teacher_info.name) != name and db_api.teacher_list(name=name):
            raise exception.ParamExist(name=name)

        phone = kwargs.get("phone", "")
        if phone and convert.bs2utf8(teacher_info.phone) != phone and db_api.teacher_list(phone=phone):
            raise exception.ParamExist(phone=phone)

        _ = db_api.teacher_update(id, kwargs)

        if kwargs.get("status", ""):
            history_values = {
                "teacher_id": id,
                "status": kwargs.get("status", "")
            }
            db_api.teacher_history_create(history_values)
        return _

    def infos(self, id="", name="",
              school_id="", school_name="",
              grade_id="", grade_name="",
              class_id="", class_name="",
              phone="", status="", position=0,
              limit=100, offset=1):
        offset = (offset - 1) * limit if offset > 0 else 0
        filters = dict()
        if id:
            filters.update({"id": id})
        if name:
            filters.update({"name": name})
        if position in (1, 2):
            filters.update({"position": position})
        if status:
            filters.update({"status": status})
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
        if phone:
            filters.update({"phone": phone})

        #关联班级名和学校名
        teacher_list = db_api.teacher_list(offset=offset, limit=limit, **filters)
        views_list = self.views(teacher_list)
        for view in views_list:
            if view.get("school_id", ""):
                school_info = db_api.school_get(id=view.get("school_id"))
                if school_info:
                    view.update({"school_name": school_info.name})
                else:
                    view.update({"school_name": ""})
            if view.get("grade_id", ""):
                grade_info = view.get("grade_info", None)
                # grade_info = db_api.grade_get(id=view.get("grade_id"))
                if grade_info:
                    view.update({"grade_name": grade_info.get("name")})
                else:
                    view.update({"grade_name": ""})

            if view.get("class_id", ""):
                class_info = view.get("class_info", None)
                # class_info = db_api.class_get(id=view.get("class_id"))
                if class_info:
                    view.update({"class_info": self.views(class_info)})
                    view.update({"class_name": class_info.get("name")})
                else:
                    view.update({"class_name": ""})

            """
            #history
            teacher_history_lilst = db_api.teacher_history_list(teacher_id=view.get("id"))
            if teacher_history_lilst:
                view.update({"status": teacher_history_lilst[0].status})
            """
        teacher_count = db_api.teacher_count(**filters)
        return {"count": teacher_count, "state": 0, "message": "query success", "data": views_list}

    def infos_for_sign(self, id="", name="",
                  school_id="",
                  grade_id="",
                  class_id="",
                  phone="", position=0,
                  sign_date="",
                  limit=100, offset=1):
        offset = (offset - 1) * limit if offset > 0 else 0
        filters = dict()
        if id:
            filters.update({"id": id})
        if name:
            filters.update({"name": name})
        if position in (1, 2):
            filters.update({"position": position})
        if school_id:
            filters.update({"school_id": school_id})
        if grade_id:
            filters.update({"grade_id": grade_id})
        if class_id:
            filters.update({"class_id": class_id})
        if phone:
            filters.update({"phone": phone})

        # 关联班级名和学校名
        teacher_list = db_api.teacher_list(offset=offset, limit=limit, **filters)

        # 关联学校和班级，还有学生得签到（学生亲属的签到信息）
        views_list = self.views(teacher_list)
        for view in views_list:
            if view.get("school_id", ""):
                school_info = db_api.school_get(id=view.get("school_id"))
                if school_info:
                    view.update({"school_name": school_info.name})
            if view.get("grade_info", None):
                grade_info = view.get("grade_info", None)
                if grade_info:
                    view.update({"grade_name": grade_info.get("name")})

            if view.get("class_info", None):
                class_info = view.get("class_info", None)
                if class_info:
                    view.update({"class_info": self.views(class_info)})

            #history
            teacher_history_lilst = db_api.teacher_history_list(teacher_id=view.get("id"))
            if teacher_history_lilst:
                view.update({"status": teacher_history_lilst[0].status})

            sign_count, late_count, early_count, sign_date = self.com_sign(view.get("id"), sign_date)
            view.update({"sign": sign_count,
                         "late": late_count,
                         "early": early_count,
                         "sign_date": datetime.datetime.strftime(sign_date, "%Y-%m")})

        teacher_count = db_api.teacher_count(**filters)
        return {"count": teacher_count, "state": 0, "message": "query success", "data": views_list}

    def info_detail_for_sign(self, id="", start_date="", end_date=""):
        if not id:
            raise exception.ParamNone(id=id)
        teacher_info = db_api.teacher_get(id)
        if not teacher_info:
            raise exception.NotFound(id=id)

        # 关联学校和班级，还有学生得签到（学生亲属的签到信息）
        teacher_info = self.views(teacher_info)
        sign_detail = self.com_sign_detail(id, start_date, end_date)
        sign_data = []
        for sign_status in sign_detail:
            sign_data.append({
                "date": datetime.datetime.strftime(sign_status.sign_date, "%Y-%m-%d"),
                "status": sign_status.status,
                "morning": sign_status.morning if sign_status.morning else "",
                "afternoon": sign_status.afternoon if sign_status.afternoon else ""
            })

        teacher_info.update({"sign_data": sign_data})
        return teacher_info

    def delete(self, id="", **kwargs):
        if not id:
            return
        db_api.teacher_deleted(id=id)
        history_values = {
            "teacher_id": id,
            "status": "deleted"
        }
        db_api.teacher_history_create(history_values)

    def info(self, id=""):
        teacher_info = db_api.teacher_get(id)
        return self.views(teacher_info)

    def info_by_phone(self, phone=""):
        if not phone:
            return
        filters = dict()
        if phone:
            filters.update({"phone": phone})

        teacher_infos = db_api.teacher_list(**filters)
        return teacher_infos

    def com_sign(self, teacher_id, sign_date=""):
        """
        统计亲属签到信息
        :param teacher_id: 教师编号
        :return:
        """
        sign_date = datetime.datetime.strptime(sign_date, "%Y-%m-%d") if convert.is_date(sign_date) else datetime.datetime.now()
        firstDay, lastDay = convert.getMonthFirstDayAndLastDay(sign_date.year, sign_date.month)
        sign_count = 0  # 出勤
        late_count = 0  # 早上迟到
        early_count = 0  # 下午早退

        sign_status_list = db_api.teacher_sign_status_list(firstDay, lastDay, teacher_id=teacher_id)
        for status_info in sign_status_list:
            if status_info.status == "11":
                sign_count += 1
            if status_info.status[0] == "2":
                late_count += 1
            if status_info.status[1] == "2":
                early_count += 1
        return sign_count, late_count, early_count, sign_date

    def com_sign_detail(self, teacher_id, start_date="", end_date=""):
        """
        :param teacher_id:
        :param start_date:
        :param end_date:
        :return:
        """
        if not convert.is_date(start_date) or not convert.is_date(end_date):
            start_date, end_date = convert.getMonthFirstDayAndLastDay(datetime.datetime.now().year, datetime.datetime.now().month)
        else:
            start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            start_date = datetime.date(start_date.year, start_date.month, start_date.day)
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
            end_date = datetime.date(end_date.year, end_date.month, end_date.day)

        sign_status_list = db_api.teacher_sign_status_list(start_date, end_date, teacher_id=teacher_id)
        return sign_status_list