#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import randint
import datetime
from util.convert import *
from util.exception import ParamExist
from util.ini_client import ini_load
from util.face_recognition_api import face_recognition_yyl
from db import api as db_api
from logic import Logic
import logging

LOG = logging.getLogger(__name__)

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
        start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        if relevance_type==2:
            #teacher
            pass

        if relevance_type in (1, 3):
            sign_list = db_api.relative_sign_list(start_time, end_time, offset, limit, relative_id=relevance_id)
            sign_count = db_api.relative_sign_count(start_time, end_time, relative_id=relevance_id)
            return {"count": sign_count, "state": 0, "message": "query success", "data": self.views(sign_list)}

        return {"count": 0, "state": 0, "message": "query success", "data": []}