#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import randint
import datetime
from util.convert import *
from db import api as db_api
from logic import Logic

class RelativeLogic(Logic):
    def __init__(self):
        pass

    def intput(self, name="", sex=0, age=0, student_code="", relation="", phone=""):
        values = {
            "name": name,
            "sex": sex,
            "age": age,
            "student_code": student_code,
            "relation": relation,
            "phone": phone
        }
        relativel_obj = db_api.relative_create(values)
        return relativel_obj

    def output(self):
        pass

    def infos(self):
        pass