#!/usr/bin/python
# -*- coding: utf-8 -*-

from db import models
from db.base import *
from db.api import model_query

def delete_student(student_id=""):
    session = get_session()
    with session.begin():
        try:
            # del relation
            query = model_query(models.RelationInfo, session=session, student_id=student_id)
            relative_ids = [relation.relative_id for relation in query.all()]
            query.delete(synchronize_session=False)

            # del student
            query = model_query(models.StudentInfo, session=session, id=student_id)
            query.update({"deleted": True},synchronize_session=False)

            # del relative
            query = model_query(models.RelativeInfo, session=session, id=relative_ids)
            query.update({"deleted": True},synchronize_session=False)
        except Exception as ex:
            session.rollback()
            raise ex