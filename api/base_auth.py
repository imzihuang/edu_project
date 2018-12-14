#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time

def auth_api_login(func):
    """
    :param func:
    :return:
    """
    def __(torn_self, *args, **kwargs):
        user_name = torn_self.get_secure_cookie('user_name')
        edu_session = torn_self.get_argument('edu_session', '')
        if not user_name and not edu_session:
            torn_self.set_status(401)
            return
        func(torn_self, *args, **kwargs)
    return __

com_cookie_time = 3600
def set_edu_cookie(set_obj, user_name, user_level, school_id=None):
    # 设置cookie
    set_obj.set_secure_cookie("user_name", user_name, expires=time.time() + com_cookie_time)
    set_obj.set_secure_cookie("user_level", str(user_level), expires=time.time() + com_cookie_time)
    if school_id:
        set_obj.set_secure_cookie("school_id", school_id, expires=time.time() + com_cookie_time)
