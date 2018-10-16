#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import randint
import datetime
from util.convert import *
from db import api as db_api

class ClassLogic():
    def __init__(self):
        pass

    def intput(self, name="", grade="", school_code="", study_number=""):
        values = {
            "name": name,
            "grade": grade,
            "school_code": school_code,
            "study_number": study_number
        }
        class_obj = db_api.class_create(values)
        return class_obj

    def output(self):
        pass

    def infos(self):
        pass