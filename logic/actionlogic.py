#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import randint
import datetime
from util.convert import *
from db import api as db_api
from logic import Logic
from util.encrypt_md5 import encry_md5

import logging
LOG = logging.getLogger(__name__)

class ActionLogic(Logic):
    def __init__(self):
        pass

    def auth_feature(self, relative_code, features):
        try:
            values = {
                "features": features
            }
            db_api.relative_update(relative_code, values)
            return True
        except Exception as ex:
            LOG.info("update relative %s feature faild:%s"%(relative_code, ex))
            return False

    def auth_username(self, name, pwd):
        filters = {
            "name": name,
            "pwd": encry_md5(pwd)
        }
        _ = db_api.user_list(**filters)
        if _:
            return True
        return False

    def auth_teacher(self, phone, pwd):
        teacher_list = db_api.teacher_list(phone=phone)
        if teacher_list:
            user_code = teacher_list[0].user_code
            _ = db_api.user_list(code=user_code, pwd=encry_md5(pwd))
            if _:
                return True
        return False


    def auth_relative(self, phone, pwd):
        relative_list = db_api.relative_list(phone=phone)
        if relative_list:
            user_code = relative_list[0].user_code
            _ = db_api.user_list(code=user_code, pwd=encry_md5(pwd))
            if _:
                return True
        return False