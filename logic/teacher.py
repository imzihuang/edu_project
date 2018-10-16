#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import randint
import datetime
from util.convert import *
from db import api as db_api

class TeacherLogic():
    def __init__(self):
        pass

    def intput(self, name="", sex=0, age=0, school_code="", class_code=""):
        values = {
            "name": name,
            "sex": sex,
            "age": age,
            "school_code": school_code,
            "class_code": class_code
        }
        teacher_obj = db_api.teacher_create(values)
        return teacher_obj

    def output(self):
        pass

    def infos(self):
        pass