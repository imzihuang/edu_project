#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import randint
import datetime
from util.convert import *
from db import api as db_api
from logic import Logic

import logging
LOG = logging.getLogger(__name__)

class RelationLogic(Logic):

    def intput(self, relation="", student_id="", relative_id=""):
        values = {
            "relation": relation,
            "student_id": student_id,
            "relative_id": relative_id
        }
        relation_obj = db_api.relation_create(values)
        return relation_obj

    def update(self, id="", **kwargs):
        if not id or not kwargs:
            return False
        _ = db_api.relation_update(id, kwargs)
        return _
