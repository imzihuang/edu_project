#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import randint
import datetime
from util.convert import *
from db import api as db_api
from logic import Logic

class StudentLogic(Logic):
    def __init__(self):
        pass

    def intput(self, name="", sex=0, age=0, grade="", school_code="", class_code="", status="apply", relation_number=3):
        values = {
            "name": name,
            "sex": sex,
            "age": age,
            "grade": grade,
            "school_code": school_code,
            "class_code": class_code,
            "status": status,
            "relation_number": relation_number
        }
        student_obj = db_api.student_create(values)
        return student_obj

    def output(self):
        pass

    def infos(self):
        pass