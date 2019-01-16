#!/usr/bin/python
# -*- coding: utf-8 -*-

from db import models
from db.base import *
from db.api import model_query
from util import common_util

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

def batch_input_teacher(teacher_data):
    """
    批量插入教师信息
    :param teacher_data: 教师信息列表
    :return:
    """
    session = get_session()
    with session.begin():
        try:
            for teacher_info in teacher_data:
                if not teacher_info.get('id'):
                    teacher_info['id'] = common_util.create_id()  # str(uuid.uuid4())
                teacher_ref = models.ClassInfo()
                teacher_ref.update(teacher_info)
                session.add(teacher_ref)
            session.commit()
        except Exception as ex:
            session.rollback()
            raise ex