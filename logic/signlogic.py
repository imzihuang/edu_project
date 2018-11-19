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

    def input(self, relevance_type=1, relevance_id=""):
        if relevance_type not in (1, 2):
            return
        values = dict()
        if relevance_type == 1:
            #家属签到
            values = {
                "relative_id": relevance_id,
                "sign_type": self.sign_type()
            }
            db_api.relation_sign_create(values)
        if relevance_type == 2:
            # 老师签到
            values = {
                "teacher_id": relevance_id,
                "sign_type": self.sign_type()
            }
            db_api.teacher_sign_create(values)

        return values

