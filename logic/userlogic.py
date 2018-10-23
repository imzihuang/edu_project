#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import randint
import datetime
from util.convert import *
from db import api as db_api
from logic import Logic

class UserLogic(Logic):
    def __init__(self):
        super(UserLogic, self).__init__()

    def intput(self, name="", sex=0, age=0, school_id="", class_id="", phone=""):
        values = {
            "name": name,
            "sex": sex,
            "age": age,
            "school_id": school_id,
            "class_id": class_id,
            "phone": phone
        }
        teacher_obj = db_api.teacher_create(values)
        return teacher_obj

class WXUserLogic(Logic):
    def __init__(self):
        super(WXUserLogic, self).__init__()

    def intput(self, name="", sex=0, age=0, school_id="", class_id="", phone=""):
        values = {
            "name": name,
            "sex": sex,
            "age": age,
            "school_id": school_id,
            "class_id": class_id,
            "phone": phone
        }
        teacher_obj = db_api.teacher_create(values)
        return teacher_obj

