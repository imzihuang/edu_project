#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import randint
from datetime import datetime
from util.encrypt_md5 import encry_md5
from util import convert
from util.exception import ParamExist
from db import api as db_api
from logic import Logic
import logging
LOG = logging.getLogger(__name__)

class VerifyManageLogic(Logic):
    def __init__(self):
        super(VerifyManageLogic, self).__init__()

    def input(self, phone="", email="", verify_code="",):
        values = {
            "verify_code": verify_code,
        }
        verify_info = None
        if phone:
            # 15 minute
            verify_info = db_api.verify_manage_get_by_phone(phone)
            _now = datetime.now()
            if verify_info and verify_info.update_time:
                if (_now - verify_info.update_time).seconds < 15 * 60:
                    # push message
                    return True
            #push message
            values.update({"phone": phone})
        if email:
            # push message
            values.update({"email": email})
        if verify_info:
            verify_obj = db_api.verify_manage_update(verify_info.id, values)
        else:
            verify_obj = db_api.verify_manage_create(values)
        return verify_obj

    def verify_code_phone(self, phone="", code=""):
        verify_info = db_api.verify_manage_get_by_phone(phone)
        if verify_info:
            _now = datetime.now()
            if convert.bs2utf8(verify_info.verify_code) == code \
                    and verify_info.update_time:
                _ = (_now - verify_info.update_time).seconds
                LOG.info("verify code time:%d"%_)
                if _ < 15*60:
                    return True
        return False


    def delete(self, id="", **kwargs):
        if not id:
            return "id is none"
        db_api.verify_manage_destroy(id=id)