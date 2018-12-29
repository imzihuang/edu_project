#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import randint
import datetime
import time
from util import convert
from util.exception import ParamExist
from util.ini_client import ini_load
from util.face_recognition_api import face_recognition_yyl
from db import api as db_api
from logic import Logic
import logging

LOG = logging.getLogger(__name__)

_conf = ini_load('config/time.ini')
_dic_con = _conf.get_fields('sign')
morning = _dic_con.get("morning")
afternoon = _dic_con.get("afternoon")

class SignLogic(Logic):
    def sign_type(self, verify_time="12:00:00"):
        now_time = time.strftime('%H:%M:%S', time.localtime(time.time()))
        if now_time>verify_time:
            return 2
        return 1

    def input(self, relevance_type=1, relevance_id="", alias="", file_path="", relevance_file_path=""):
        if relevance_type not in (1, 2, 3):
            return
        values = dict()
        if relevance_type in (1, 3):
            #家属签到
            _sign_type = self.sign_type()
            values = {
                "relative_id": relevance_id,
                "type": _sign_type,
                "alias": alias,
                "img_path": file_path,
                "relative_img_path": relevance_file_path,
            }
            _ = db_api.relative_sign_create(values)
            if _:
                student_id = self._get_student_id_by_relative(relative_id=relevance_id)
                self.manage_student_sign_status(student_id, _sign_type)

        if relevance_type == 2:
            # 老师签到
            _sign_type = self.sign_type()
            values = {
                "teacher_id": relevance_id,
                "type": _sign_type,
                "alias": alias,
                "img_path": file_path,
                "teacher_img_path": relevance_file_path,
            }
            _ = db_api.teacher_sign_create(values)
            if _:
                self.manage_teacher_sign_status(relevance_id, _sign_type)

        return values

    def infos(self, relevance_type=1, relevance_id="", start_time="", end_time="", limit=100, offset=0):
        offset = (offset - 1) * limit if offset > 0 else 0
        start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        if relevance_type==2:
            sign_list = db_api.teacher_sign_list(start_time, end_time, offset, limit, teacher_id=relevance_id)
            view_list = self.views(sign_list)
            if not view_list:
                return {"count": 0, "state": 0, "message": "query teacher success", "data": []}
            for view in view_list:
                view.update({"img_path": "image/tmp/" + view.get("img_path", "")})
                view.update({"teacher_img_path": "image/face/" + view.get("teacher_img_path", "")})

            sign_count = db_api.teacher_sign_count(start_time, end_time, teacher_id=relevance_id)
            return {"count": sign_count, "state": 0, "message": "query success", "data": view_list}

        if relevance_type in (1, 3):
            sign_list = db_api.relative_sign_list(start_time, end_time, offset, limit, relative_id=relevance_id)
            view_list = self.views(sign_list)
            if not view_list:
                return {"count": 0, "state": 0, "message": "query relative success", "data": []}
            for view in view_list:
                view.update({"img_path": "image/tmp/" + view.get("img_path", "")})
                view.update({"relative_img_path": "image/face/" + view.get("relative_img_path", "")})

            sign_count = db_api.relative_sign_count(start_time, end_time, relative_id=relevance_id)
            return {"count": sign_count, "state": 0, "message": "query success", "data": view_list}

        return {"count": 0, "state": 0, "message": "query success", "data": []}

    def manage_student_sign_status(self, student_id, sign_type):
        """
        更新考勤信息,status:
        上午只认第一次打卡，下午每次签到都要做一次判断，直到最后一次。
        10：上午正常打卡，下午未打卡
        20：上午迟到，下午未打卡
        01：上午未打卡，下午正常打卡
        02：上午未打卡，下午早退
        11：出勤
        12：上午正常打卡，下午早退
        21：上午迟到，下午正常打卡
        22: 上午迟到，下午早退
        :param relevance_id:
        :param sign_type:
        :return:
        """
        # 判断下上午是否打卡了
        today = datetime.date.today()
        now_time = time.strftime('%H:%M:%S', time.localtime(time.time()))
        sign_status_list = db_api.student_sign_status_list(today, today, student_id=student_id)
        if sign_type == 1:
            if sign_status_list:
                #上午只认第一次打卡
                return
            status = "10" if now_time < morning else "20"
            values = {
                "student_id": student_id,
                "sign_date": datetime.date.today(),
                "status": status,
                "morning": now_time,
            }
            db_api.student_sign_status_create(values)
        if sign_type == 2:
            if sign_status_list:
                # 早于下午时间点，正常打卡。否则，下午早退
                status_2 = "1" if now_time > afternoon else "2"
                status = sign_status_list[0].status[0]+status_2
                db_api.student_sign_status_update(sign_status_list[0].id, {"status": status, "afternoon": now_time})
            else:
                # 不存在存在上午打卡，状态改为出勤
                LOG.info("now after:%s, %s"%(now_time, afternoon))
                status = "01" if now_time > afternoon else "02"
                values = {
                    "student_id": student_id,
                    "sign_date": datetime.date.today(),
                    "status": status,
                    "afternoon": now_time
                }
                db_api.student_sign_status_create(values)

    def _get_student_id_by_relative(self, relative_id):
        if relative_id:
            _relation_list = db_api.relation_list(relative_id=relative_id)
            relation_info = _relation_list[0]
            return relation_info.student_id

    def manage_teacher_sign_status(self, teacher_id, sign_type):
        """
        更新考勤信息,status:
        上午只认第一次打卡，下午每次签到都要做一次判断，直到最后一次。
        10：上午正常打卡，下午未打卡
        20：上午迟到，下午未打卡
        01：上午未打卡，下午正常打卡
        02：上午未打卡，下午早退
        11：出勤
        12：上午正常打卡，下午早退
        21：上午迟到，下午正常打卡
        22: 上午迟到，下午早退
        :param relevance_id:
        :param sign_type:
        :return:
        """
        # 判断下上午是否打卡了
        today = datetime.date.today()
        now_time = time.strftime('%H:%M:%S', time.localtime(time.time()))
        sign_status_list = db_api.teacher_sign_status_list(today, today, teacher_id=teacher_id)
        if sign_type == 1:
            if sign_status_list:
                #上午只认第一次打卡
                return
            status = "10" if now_time < morning else "20"
            values = {
                "teacher_id": teacher_id,
                "sign_date": datetime.date.today(),
                "status": status,
                "morning": now_time,
            }
            db_api.teacher_sign_status_create(values)
        if sign_type == 2:
            if sign_status_list:
                # 早于下午时间点，正常打卡。否则，下午早退
                status_2 = "1" if now_time > afternoon else "2"
                status = sign_status_list[0].status[0]+status_2
                db_api.teacher_sign_status_update(sign_status_list[0].id, {"status": status, "afternoon": now_time})
            else:
                # 不存在存在上午打卡，状态改为出勤
                LOG.info("now after:%s, %s"%(now_time, afternoon))
                status = "01" if now_time > afternoon else "02"
                values = {
                    "teacher_id": teacher_id,
                    "sign_date": datetime.date.today(),
                    "status": status,
                    "afternoon": now_time
                }
                db_api.teacher_sign_status_create(values)


