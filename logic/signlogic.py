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

    def input(self, relevance_type=1, relevance_id="", alias=""):
        if relevance_type not in (1, 2, 3):
            return
        values = dict()
        if relevance_type in (1, 3):
            #家属签到
            values = {
                "relative_id": relevance_id,
                "sign_type": self.sign_type(),
                "alias": alias
            }
            db_api.relative_sign_create(values)

        if relevance_type == 2:
            # 老师签到
            values = {
                "teacher_id": relevance_id,
                "sign_type": self.sign_type(),
                "alias": alias
            }
            db_api.teacher_sign_create(values)

        return values

    def infos(self, relevance_type=1, relevance_id="", start_time="", end_time="", limit=100, offset=1):
        start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        if relevance_type==2:
            #teacher
            pass

        if relevance_type in (1, 3):
            sign_list = db_api.relative_sign_list(start_time, end_time, offset, limit, relative_id=relevance_id)
            sign_count = db_api.relative_sign_count(start_time, end_time, relative_id=relevance_id)
            return {"count": sign_count, "state": 0, "message": "query success", "data": self.views(sign_list)}

        return {"count": 0, "state": 0, "message": "query success", "data": []}

    def manage_relative_sign_status(self, relative_id, sign_type, ):
        """
        更新考勤信息,status:
        10：上午打卡
        20：上午迟到
        01：上午未打卡，下午打卡
        02：上午未打卡，下午早退
        11：出勤
        22: 上午迟到，下午早退
        :param relevance_id:
        :param sign_type:
        :return:
        """
        # 判断下上午是否打卡了
        today = datetime.date.today()
        now_time = time.strftime('%H:%M:%S', time.localtime(time.time()))
        # tomorrow = today + datetime.timedelta(days=1)
        sign_list = db_api.relative_sign_status_list(today, today, relative_id=relative_id)
        if sign_type == 1:
            if sign_list:
                return
            status = "10" if now_time < morning else "20"
            values = {
                "relative_id": relative_id,
                "sign_date": datetime.date.today(),
                "status": status
            }
            db_api.relative_sign_status_create(values)
        if sign_type == 2:
            if sign_list:
                #存在上午打卡，状态改为出勤
                if sign_list[0].status == "10":
                    status = "11" if now_time>afternoon else status = "12"
                    db_api.relative_sign_status_update(sign_list[0].id, {"status": status})
                else:#上午迟到
                    status = "21" if now_time > afternoon else status = "22"
                    db_api.relative_sign_status_update(sign_list[0].id, {"status": status})
            else:
                # 存在上午打卡，状态改为出勤
                values = {
                    "relative_id": relative_id,
                    "sign_date": datetime.date.today(),
                    "status": 3
                }
                db_api.relative_sign_status_create(values)

