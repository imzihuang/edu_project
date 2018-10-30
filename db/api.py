#!/usr/bin/python
# -*- coding: utf-8 -*-

import uuid
from db import models
from db.base import *
from util import exception


def model_query(model, session=None,  *args, **kwargs):
    """
    :param model:
    :param session: if present, the session to use
    """
    session = session or get_session()
    query = session.query(model, *args)
    filter_dict = {}
    for key, value in kwargs.items():
        if isinstance(value, (list, tuple, set, frozenset)):
            column_attr = getattr(model, key)
            query = query.filter(column_attr.in_(value))
        else:
            filter_dict[key] = value

    if filter_dict:
        query = query.filter_by(**filter_dict)

    return query

#####################school begin################################
def school_create(values):
    if not values.get('id'):
        values['id'] = str(uuid.uuid4())
    school_ref = models.SchoolInfo()
    school_ref.update(values)
    session = get_session()
    with session.begin():
        school_ref.save(session)
        return school_ref

def school_update(id, values):
    query = model_query(models.SchoolInfo).filter_by(id=id)
    result = query.update(values)
    if not result:
        raise exception.NotFound(code=id)
    return result

def school_get(id):
    query = model_query(models.SchoolInfo)
    result = query.filter_by(id=id).first()
    if not result:
        raise exception.NotFound(code=id)
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
    if not values.get('id'):
        values['id'] = str(uuid.uuid4())
    class_ref = models.ClassInfo()
    class_ref.update(values)
    session = get_session()
    with session.begin():
        class_ref.save(session)
        return class_ref

def class_update(id, values):
    query = model_query(models.ClassInfo).filter_by(id=id)
    result = query.update(values)
    if not result:
        raise exception.NotFound(code=id)
    return result

def class_get(id):
    query = model_query(models.ClassInfo)
    result = query.filter_by(id=id).first()
    if not result:
        raise exception.NotFound(code=id)
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
    if not values.get('id'):
        values['id'] = str(uuid.uuid4())
    teacher_ref = models.TeacherInfo()
    teacher_ref.update(values)
    session = get_session()
    with session.begin():
        teacher_ref.save(session)
        return teacher_ref

def teacher_update(id, values):
    query = model_query(models.TeacherInfo).filter_by(id=id)
    result = query.update(values)
    if not result:
        raise exception.NotFound(code=id)
    return result

def teacher_get(id):
    query = model_query(models.TeacherInfo)
    result = query.filter_by(id=id).first()
    if not result:
        raise exception.NotFound(code=id)
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
    if not values.get('id'):
        values['id'] = str(uuid.uuid4())
    student_ref = models.StudentInfo()
    student_ref.update(values)
    session = get_session()
    with session.begin():
        student_ref.save(session)
        return student_ref

def student_update(id, values):
    query = model_query(models.StudentInfo).filter_by(id=id)
    result = query.update(values)
    if not result:
        raise exception.NotFound(code=id)
    return result

def student_get(id):
    query = model_query(models.StudentInfo)
    result = query.filter_by(id=id).first()
    if not result:
        raise exception.NotFound(code=id)
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
    if not values.get('id'):
        values['id'] = str(uuid.uuid4())
    relative_ref = models.RelativeInfo()
    relative_ref.update(values)
    session = get_session()
    with session.begin():
        relative_ref.save(session)
        return relative_ref

def relative_update(id, values):
    query = model_query(models.RelativeInfo).filter_by(id=id)
    result = query.update(values)
    if not result:
        raise exception.NotFound(id=id)
    return result

def relative_get(id):
    query = model_query(models.RelativeInfo)
    result = query.filter_by(id=id).first()
    if not result:
        raise exception.NotFound(code=id)
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

def relative_face_auth(values):
    session = get_session()
    query = model_query(models.RelativeFeature, session=session).filter_by(relative_id=values.get("relative_id"))
    if query:
        result = query.update(values)
        return result
    relative_ref = models.RelativeFeature()
    relative_ref.update(values)
    with session.begin():
        relative_ref.save(session)
        return relative_ref


#####################relative end################################


#####################relative_feature begin################################
def feature_create(values):
    if not values.get('id'):
        values['id'] = str(uuid.uuid4())
    relation_ref = models.RelativeFeature()
    relation_ref.update(values)
    session = get_session()
    with session.begin():
        relation_ref.save(session)
        return relation_ref

def feature_update(id, values):
    query = model_query(models.RelativeFeature).filter_by(id=id)
    result = query.update(values)
    if not result:
        raise exception.NotFound(code=id)
    return result

def feature_get(id):
    query = model_query(models.RelativeFeature)
    result = query.filter_by(id=id).first()
    if not result:
        raise exception.NotFound(code=id)
    return result

def feature_list(offset=0, limit=1000, **filters):
    query = model_query(models.RelativeFeature, **filters)
    if offset:
        query.offset(offset)
    if limit:
        query.limit(limit)
    return query.all()

def feature_count(**filters):
    query = model_query(models.RelativeFeature, **filters)
    return query.count()
#####################relative_feature end################################


#####################relation begin################################
def relation_create(values):
    if not values.get('id'):
        values['id'] = str(uuid.uuid4())
    relation_ref = models.RelationInfo()
    relation_ref.update(values)
    session = get_session()
    with session.begin():
        relation_ref.save(session)
        return relation_ref

def relation_update(id, values):
    query = model_query(models.RelationInfo).filter_by(id=id)
    result = query.update(values)
    if not result:
        raise exception.NotFound(code=id)
    return result

def relation_get(id):
    query = model_query(models.RelationInfo)
    result = query.filter_by(id=id).first()
    if not result:
        raise exception.NotFound(code=id)
    return result

def relation_list(offset=0, limit=1000, **filters):
    query = model_query(models.RelationInfo, **filters)
    if offset:
        query.offset(offset)
    if limit:
        query.limit(limit)
    return query.all()

def relation_count(**filters):
    query = model_query(models.RelationInfo, **filters)
    return query.count()
#####################relation end################################

#####################user begin################################
def user_create(values):
    if not values.get('id'):
        values['id'] = str(uuid.uuid4())
    user_ref = models.UserInfo()
    user_ref.update(values)
    session = get_session()
    with session.begin():
        user_ref.save(session)
        return user_ref

def user_update(id, values):
    query = model_query(models.UserInfo).filter_by(id=id)
    result = query.update(values)
    if not result:
        raise exception.NotFound(code=id)
    return result

def user_get(id):
    query = model_query(models.UserInfo)
    result = query.filter_by(id=id).first()
    if not result:
        raise exception.NotFound(code=id)
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

#####################wx user begin################################
def wxuser_create(values):
    if not values.get('id'):
        values['id'] = str(uuid.uuid4())
    wxuser_ref = models.WXUserInfo()
    wxuser_ref.update(values)
    session = get_session()
    with session.begin():
        wxuser_ref.save(session)
        return wxuser_ref

def wxuser_update(id, values):
    query = model_query(models.WXUserInfo).filter_by(id=id)
    result = query.update(values)
    if not result:
        raise exception.NotFound(code=id)
    return result

def wxuser_get(id):
    query = model_query(models.WXUserInfo)
    result = query.filter_by(id=id).first()
    if not result:
        raise exception.NotFound(code=id)
    return result

def wxuser_list(offset=0, limit=1000, **filters):
    query = model_query(models.WXUserInfo, **filters)
    if offset:
        query.offset(offset)
    if limit:
        query.limit(limit)
    return query.all()

def wxuser_count(**filters):
    query = model_query(models.WXUserInfo, **filters)
    return query.count()

#####################user end################################