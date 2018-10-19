#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
from db.base import *
from db import models
import exception


def model_query(model, session=None, *args, **kwargs):
    """
    :param model:
    :param session: if present, the session to use
    """
    session = session or get_session()
    query = session.query(model, *args)
    if kwargs:
        query = query.filter_by(**kwargs)

    return query

#####################school begin################################
def school_create(values):
    school_ref = models.SchoolInfo()
    school_ref.update(values)
    session = get_session()
    with session.begin():
        school_ref.save(session)
        return school_ref

def school_update(code, values):
    query = model_query(models.SchoolInfo).filter_by(code=code)
    result = query.update(values)
    if not result:
        raise exception.NotFound(code=code)

def school_get(code):
    query = model_query(models.SchoolInfo)
    result = query.filter_by(code=code).first()
    if not result:
        raise exception.NotFound(code=code)
    return result

def school_list(offset=0, limit=1000, **filters):
    query = model_query(models.SchoolInfo, **filters)
    if offset:
        query.offset(offset)
    if limit:
        query.limit(limit)
    return query.all()

def school_count(**filters):
    query = model_query(models.SchoolInfo, **filters)
    return query.count()

#####################school end################################

#####################class begin################################
def class_create(values):
    class_ref = models.ClassInfo()
    class_ref.update(values)
    session = get_session()
    with session.begin():
        class_ref.save(session)
        return class_ref

def class_update(code, values):
    query = model_query(models.ClassInfo).filter_by(code=code)
    result = query.update(values)
    if not result:
        raise exception.NotFound(code=code)

def class_get(code):
    query = model_query(models.ClassInfo)
    result = query.filter_by(code=code).first()
    if not result:
        raise exception.NotFound(code=code)
    return result

def class_list(offset=0, limit=1000, **filters):
    query = model_query(models.ClassInfo, **filters)
    if offset:
        query.offset(offset)
    if limit:
        query.limit(limit)
    return query.all()

def class_count(**filters):
    query = model_query(models.ClassInfo, **filters)
    return query.count()

#####################class end################################

#####################teacher begin################################
def teacher_create(values):
    class_ref = models.TeacherInfo()
    class_ref.update(values)
    session = get_session()
    with session.begin():
        class_ref.save(session)
        return class_ref

def teacher_update(code, values):
    query = model_query(models.TeacherInfo).filter_by(code=code)
    result = query.update(values)
    if not result:
        raise exception.NotFound(code=code)

def teacher_get(code):
    query = model_query(models.TeacherInfo)
    result = query.filter_by(code=code).first()
    if not result:
        raise exception.NotFound(code=code)
    return result

def teacher_list(offset=0, limit=1000, **filters):
    query = model_query(models.TeacherInfo, **filters)
    if offset:
        query.offset(offset)
    if limit:
        query.limit(limit)
    return query.all()

def teacher_count(**filters):
    query = model_query(models.TeacherInfo, **filters)
    return query.count()

#####################class end################################

#####################student begin################################
def student_create(values):
    class_ref = models.StudentInfo()
    class_ref.update(values)
    session = get_session()
    with session.begin():
        class_ref.save(session)
        return class_ref

def student_update(code, values):
    query = model_query(models.StudentInfo).filter_by(code=code)
    result = query.update(values)
    if not result:
        raise exception.NotFound(code=code)

def student_get(code):
    query = model_query(models.StudentInfo)
    result = query.filter_by(code=code).first()
    if not result:
        raise exception.NotFound(code=code)
    return result

def student_list(offset=0, limit=1000, **filters):
    query = model_query(models.StudentInfo, **filters)
    if offset:
        query.offset(offset)
    if limit:
        query.limit(limit)
    return query.all()

def student_count(**filters):
    query = model_query(models.StudentInfo, **filters)
    return query.count()

#####################student end################################

#####################relative begin################################
def relative_create(values):
    class_ref = models.RelativeInfo()
    class_ref.update(values)
    session = get_session()
    with session.begin():
        class_ref.save(session)
        return class_ref

def relative_update(code, values):
    query = model_query(models.RelativeInfo).filter_by(code=code)
    result = query.update(values)
    if not result:
        raise exception.NotFound(code=code)

def relative_get(code):
    query = model_query(models.RelativeInfo)
    result = query.filter_by(code=code).first()
    if not result:
        raise exception.NotFound(code=code)
    return result

def relative_list(offset=0, limit=1000, **filters):
    query = model_query(models.RelativeInfo, **filters)
    if offset:
        query.offset(offset)
    if limit:
        query.limit(limit)
    return query.all()

def relative_count(**filters):
    query = model_query(models.RelativeInfo, **filters)
    return query.count()

#####################relative end################################


#####################user begin################################
def user_create(values):
    class_ref = models.UserInfo()
    class_ref.update(values)
    session = get_session()
    with session.begin():
        class_ref.save(session)
        return class_ref

def user_update(code, values):
    query = model_query(models.UserInfo).filter_by(code=code)
    result = query.update(values)
    if not result:
        raise exception.NotFound(code=code)

def user_get(code):
    query = model_query(models.UserInfo)
    result = query.filter_by(code=code).first()
    if not result:
        raise exception.NotFound(code=code)
    return result

def user_list(offset=0, limit=1000, **filters):
    query = model_query(models.UserInfo, **filters)
    if offset:
        query.offset(offset)
    if limit:
        query.limit(limit)
    return query.all()

def user_count(**filters):
    query = model_query(models.UserInfo, **filters)
    return query.count()

#####################user end################################