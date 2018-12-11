#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import or_, and_
from db import models
from db.base import *
from util import exception
from util import common_util


def model_query(model, session=None, order=False, read_deleted="no", desc=True, *args, **kwargs):
    """
    :param model:
    :param session: if present, the session to use
    """
    session = session or get_session()
    query = session.query(model, *args)

    if read_deleted == "no":
        query = query.filter_by(deleted=False)

    filter_dict = {}
    for key, value in kwargs.items():
        if isinstance(value, (list, tuple, set, frozenset)):
            column_attr = getattr(model, key)
            query = query.filter(column_attr.in_(value))
        else:
            filter_dict[key] = value

    if filter_dict:
        query = query.filter_by(**filter_dict)
    if order:
        if desc:
            query = query.order_by(model.create_time.desc())
        else:
            query = query.order_by(model.create_time)

    return query

#####################school begin################################
def school_create(values):
    if not values.get('id'):
        values['id'] = common_util.create_id()#str(uuid.uuid4())
    school_ref = models.SchoolInfo()
    school_ref.update(values)
    session = get_session()
    with session.begin():
        school_ref.save(session)
        return values

def school_update(id, values):
    query = model_query(models.SchoolInfo).filter_by(id=id)
    result = query.update(values)
    if not result:
        return None  #raise exception.NotFound(code=id)
    return result

def school_get(id):
    query = model_query(models.SchoolInfo)
    result = query.filter_by(id=id).first()
    if not result:
        return None  #raise exception.NotFound(code=id)
    return result

def school_list(offset=0, limit=1000, **filters):
    query = model_query(models.SchoolInfo, order=True, **filters)
    if offset:
        query = query.offset(offset)
    if limit:
        query = query.limit(limit)
    return query.all()

def school_count(**filters):
    query = model_query(models.SchoolInfo, **filters)
    return query.count()

def school_deleted(id):
    session = get_session()
    with session.begin():
        query = model_query(models.SchoolInfo, session=session, id=id)
        query.update({
            "deleted": True
        },
        synchronize_session=False)

#####################school end################################

#####################grade begin################################
def grade_create(values):
    if not values.get('id'):
        values['id'] = common_util.create_id()#str(uuid.uuid4())
    grade_ref = models.GradeInfo()
    grade_ref.update(values)
    session = get_session()
    with session.begin():
        grade_ref.save(session)
        return values

def grade_update(id, values):
    query = model_query(models.GradeInfo).filter_by(id=id)
    result = query.update(values)
    if not result:
        return None#raise exception.NotFound(code=id)
    return result

def grade_get(id):
    query = model_query(models.GradeInfo)
    result = query.filter_by(id=id).first()
    if not result:
        return None#raise exception.NotFound(code=id)
    return result

def grade_list(offset=0, limit=1000, **filters):
    query = model_query(models.GradeInfo, order=True, **filters)
    if offset:
        query = query.offset(offset)
    if limit:
        query = query.limit(limit)
    return query.all()

def grade_count(**filters):
    query = model_query(models.GradeInfo, **filters)
    return query.count()

def grade_deleted(id):
    session = get_session()
    with session.begin():
        query = model_query(models.GradeInfo, session=session, id=id)
        query.update({
            "deleted": True
        },
        synchronize_session=False)

#####################grade end################################

#####################class begin################################
def class_create(values):
    if not values.get('id'):
        values['id'] = common_util.create_id()
    class_ref = models.ClassInfo()
    class_ref.update(values)
    session = get_session()
    with session.begin():
        class_ref.save(session)
        return values

def class_update(id, values):
    query = model_query(models.ClassInfo).filter_by(id=id)
    result = query.update(values)
    if not result:
        return None  #raise exception.NotFound(code=id)
    return result

def class_get(id):
    query = model_query(models.ClassInfo)
    result = query.filter_by(id=id).first()
    if not result:
        return None  #raise exception.NotFound(code=id)
    return result

def class_list(offset=0, limit=1000, **filters):
    query = model_query(models.ClassInfo, order=True, **filters)
    if offset:
        query = query.offset(offset)
    if limit:
        query = query.limit(limit)
    return query.all()

def class_count(**filters):
    query = model_query(models.ClassInfo, **filters)
    return query.count()

def class_deleted(id):
    session = get_session()
    with session.begin():
        query = model_query(models.ClassInfo, session=session, id=id)
        query.update({
            "deleted": True
        },
        synchronize_session=False)

#####################class end################################

#####################teacher begin################################
def teacher_create(values):
    if not values.get('id'):
        values['id'] = common_util.create_id()
    teacher_ref = models.TeacherInfo()
    teacher_ref.update(values)
    session = get_session()
    with session.begin():
        teacher_ref.save(session)
        return values

def teacher_update(id, values):
    query = model_query(models.TeacherInfo).filter_by(id=id)
    result = query.update(values)
    if not result:
        return None  #raise exception.NotFound(code=id)
    return result

def teacher_get(id):
    query = model_query(models.TeacherInfo, read_deleted="yes")
    result = query.filter_by(id=id).first()
    if not result:
        return None  #raise exception.NotFound(code=id)
    return result

def teacher_list(offset=0, limit=1000, **filters):
    query = model_query(models.TeacherInfo, order=True, **filters)
    if offset:
        query = query.offset(offset)
    if limit:
        query = query.limit(limit)
    return query.all()

def teacher_count(**filters):
    query = model_query(models.TeacherInfo, **filters)
    return query.count()

def teacher_deleted(id):
    session = get_session()
    with session.begin():
        query = model_query(models.TeacherInfo, session=session, id=id)
        query.update({
            "deleted": True
        },
        synchronize_session=False)

def teacher_history_create(values):
    if not values.get('id'):
        values['id'] = common_util.create_id()
    teacherhistory_ref = models.TeacherHistory()
    teacherhistory_ref.update(values)
    session = get_session()
    with session.begin():
        teacherhistory_ref.save(session)
        return values

def teacher_history_list(offset=0, limit=1000, **filters):
    query = model_query(models.TeacherHistory, **filters)
    if offset:
        query = query.offset(offset)
    if limit:
        query = query.limit(limit)
    return query.all()

def teacher_history_count(**filters):
    query = model_query(models.TeacherHistory, **filters)
    return query.count()

#####################teacher end################################

#####################student begin################################
def student_create(values):
    if not values.get('id'):
        values['id'] = common_util.create_id()
    student_ref = models.StudentInfo()
    student_ref.update(values)
    session = get_session()
    with session.begin():
        student_ref.save(session)
        return values

def student_update(id, values):
    query = model_query(models.StudentInfo).filter_by(id=id)
    result = query.update(values)
    if not result:
        return None  #raise exception.NotFound(code=id)
    return result

def student_get(id):
    query = model_query(models.StudentInfo, read_deleted="yes")
    result = query.filter_by(id=id).first()
    if not result:
        return None  #raise exception.NotFound(code=id)
    return result

def student_list(offset=0, limit=1000, **filters):
    query = model_query(models.StudentInfo, order=True, **filters)
    if offset:
        query = query.offset(offset)
    if limit:
        query = query.limit(limit)
    return query.all()

def student_count(**filters):
    query = model_query(models.StudentInfo, **filters)
    return query.count()

def student_history_create(values):
    if not values.get('id'):
        values['id'] = common_util.create_id()
    studenthistory_ref = models.StudentHistory()
    studenthistory_ref.update(values)
    session = get_session()
    with session.begin():
        studenthistory_ref.save(session)
        return values

def student_history_list(offset=0, limit=1000, **filters):
    query = model_query(models.StudentHistory, **filters)
    if offset:
        query = query.offset(offset)
    if limit:
        query = query.limit(limit)
    return query.all()

def student_history_count(**filters):
    query = model_query(models.StudentHistory, **filters)
    return query.count()

def student_deleted(id):
    session = get_session()
    with session.begin():
        query = model_query(models.StudentInfo, session=session, id=id)
        query.update({
            "deleted": True
        },
        synchronize_session=False)

#####################student end################################

#####################relative begin################################
def relative_create(values):
    if not values.get('id'):
        values['id'] = common_util.create_id()
    relative_ref = models.RelativeInfo()
    relative_ref.update(values)
    session = get_session()
    with session.begin():
        relative_ref.save(session)
        return values

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
        return None  #raise exception.NotFound(code=id)
    return result

def relative_list(offset=0, limit=1000, **filters):
    query = model_query(models.RelativeInfo, order=True, **filters)
    if offset:
        query = query.offset(offset)
    if limit:
        query = query.limit(limit)
    return query.all()

def relative_count(**filters):
    query = model_query(models.RelativeInfo, **filters)
    return query.count()

def relative_deleted(id):
    session = get_session()
    with session.begin():
        query = model_query(models.RelativeInfo, session=session, id=id)
        query.update({
            "deleted": True
        },
        synchronize_session=False)

#####################relative end################################

#####################face begin################################
def face_create(values):
    if not values.get('id'):
        values['id'] = common_util.create_id()
    face_ref = models.RelevanceFace()
    face_ref.update(values)
    session = get_session()
    with session.begin():
        face_ref.save(session)
        return values

def face_get(id):
    query = model_query(models.RelevanceFace)
    result = query.filter_by(id=id).first()
    if not result:
        return None
    return result

def face_list(offset=0, limit=1000, **filters):
    query = model_query(models.RelevanceFace, order=True, desc=False, **filters)
    if offset:
        query = query.offset(offset)
    if limit:
        query = query.limit(limit)
    return query.all()

def face_count(**filters):
    query = model_query(models.RelevanceFace, **filters)
    return query.count()

def face_update(id, values):
    query = model_query(models.RelevanceFace).filter_by(id=id)
    result = query.update(values)
    if not result:
        raise exception.NotFound(id=id)
    return result

def face_destroy(id):
    session = get_session()
    with session.begin():
        query = model_query(models.RelevanceFace, session=session, id=id)
        query.delete(synchronize_session=False)

#####################face end################################


#####################relation begin################################
def relation_create(values):
    if not values.get('id'):
        values['id'] = common_util.create_id()
    relation_ref = models.RelationInfo()
    relation_ref.update(values)
    session = get_session()
    with session.begin():
        relation_ref.save(session)
        return values

def relation_update(id, values):
    query = model_query(models.RelationInfo).filter_by(id=id)
    result = query.update(values)
    if not result:
        return None  #raise exception.NotFound(code=id)
    return result

def relation_get(id):
    query = model_query(models.RelationInfo)
    result = query.filter_by(id=id).first()
    if not result:
        return None  #raise exception.NotFound(code=id)
    return result

def relation_list(offset=0, limit=1000, **filters):
    query = model_query(models.RelationInfo, order=True, **filters)
    if offset:
        query = query.offset(offset)
    if limit:
        query = query.limit(limit)
    return query.all()

def relation_count(**filters):
    query = model_query(models.RelationInfo, **filters)
    return query.count()

def relation_destroy(id):
    session = get_session()
    with session.begin():
        query = model_query(models.RelationInfo, session=session, id=id)
        query.delete(synchronize_session=False)
#####################relation end################################

#####################user begin################################
def user_create(values):
    if not values.get('id'):
        values['id'] = common_util.create_id()
    user_ref = models.UserInfo()
    user_ref.update(values)
    session = get_session()
    with session.begin():
        user_ref.save(session)
        return values

def user_update(id, values):
    query = model_query(models.UserInfo).filter_by(id=id)
    result = query.update(values)
    if not result:
        return None  #raise exception.NotFound(code=id)
    return result

def user_get(id):
    query = model_query(models.UserInfo)
    result = query.filter_by(id=id).first()
    if not result:
        return None  #raise exception.NotFound(code=id)
    return result

def user_list(offset=0, limit=1000, **filters):
    query = model_query(models.UserInfo, order=True, **filters)
    if offset:
        query = query.offset(offset)
    if limit:
        query = query.limit(limit)
    return query.all()

def user_count(**filters):
    query = model_query(models.UserInfo, **filters)
    return query.count()

def user_deleted(id):
    session = get_session()
    with session.begin():
        query = model_query(models.UserInfo, session=session, id=id)
        query.update({
            "deleted": True
        },
        synchronize_session=False)

#####################user end################################

#####################wx user begin################################
def wxuser_create(values):
    if not values.get('id'):
        values['id'] = common_util.create_id()
    wxuser_ref = models.WXUserInfo()
    wxuser_ref.update(values)
    session = get_session()
    with session.begin():
        wxuser_ref.save(session)
        return values

def wxuser_update(id, values):
    query = model_query(models.WXUserInfo).filter_by(id=id)
    result = query.update(values)
    if not result:
        return None  #raise exception.NotFound(code=id)
    return result

def wxuser_get(id):
    query = model_query(models.WXUserInfo)
    result = query.filter_by(id=id).first()
    if not result:
        return None  #raise exception.NotFound(code=id)
    return result

def wxuser_list(offset=0, limit=1000, **filters):
    query = model_query(models.WXUserInfo, order=True, **filters)
    if offset:
        query = query.offset(offset)
    if limit:
        query = query.limit(limit)
    return query.all()

def wxuser_count(**filters):
    query = model_query(models.WXUserInfo, **filters)
    return query.count()

def wxuser_deleted(id):
    session = get_session()
    with session.begin():
        query = model_query(models.WXUserInfo, session=session, id=id)
        query.update({
            "deleted": True
        },
        synchronize_session=False)

#####################wx user end################################

#################sign start#####################################
def relative_sign_create(values):
    if not values.get('id'):
        values['id'] = common_util.create_id()
    relation_sign_ref = models.RelativeSignInfo()
    relation_sign_ref.update(values)
    session = get_session()
    with session.begin():
        relation_sign_ref.save(session)
        return values

def relative_sign_list(start_time, end_time, offset=0, limit=1000, **filters):
    query = model_query(models.RelativeSignInfo, order=True, **filters)
    query = query.filter(and_(models.RelativeSignInfo.create_time < end_time,
                              models.RelativeSignInfo.create_time > start_time))
    if offset:
        query = query.offset(offset)
    if limit:
        query = query.limit(limit)
    return query.all()

def relative_sign_count(start_time, end_time, **filters):
    query = model_query(models.RelativeSignInfo, **filters)
    query = query.filter(models.RelativeSignInfo.create_time < end_time). \
        filter(models.RelativeSignInfo.create_time > start_time)
    return query.count()

def teacher_sign_create(values):
    if not values.get('id'):
        values['id'] = common_util.create_id()
    teacher_sign_ref = models.TeacherSignInfo()
    teacher_sign_ref.update(values)
    session = get_session()
    with session.begin():
        teacher_sign_ref.save(session)
        return values

#################sign end#######################################

#################sign status start###################################
def relative_sign_status_create(values):
    if not values.get('id'):
        values['id'] = common_util.create_id()
    relation_sign_ref = models.RelativeStatusInfo()
    relation_sign_ref.update(values)
    session = get_session()
    with session.begin():
        relation_sign_ref.save(session)
        return values

def relative_sign_status_update(id, values):
    query = model_query(models.RelativeStatusInfo).filter_by(id=id)
    result = query.update(values)
    if not result:
        return None  #raise exception.NotFound(code=id)
    return result

def relative_sign_status_list(start_time, end_time, offset=0, limit=1000, **filters):
    query = model_query(models.RelativeStatusInfo, order=True, **filters)
    query = query.filter(models.RelativeStatusInfo.sign_date<=end_time).\
        filter(models.RelativeStatusInfo.sign_date>=start_time)
    if offset:
        query = query.offset(offset)
    if limit:
        query = query.limit(limit)
    return query.all()
#################sign status end#####################################


#################verify manage start#####################################
def verify_manage_create(values):
    if not values.get('id'):
        values['id'] = common_util.create_id()
    verify_ref = models.VerifyManage()
    verify_ref.update(values)
    session = get_session()
    with session.begin():
        verify_ref.save(session)
        return values

def verify_manage_get(id):
    query = model_query(models.VerifyManage)
    result = query.filter_by(id=id).first()
    if not result:
        return None
    return result

def verify_manage_get_by_phone(phone):
    query = model_query(models.VerifyManage)
    result = query.filter_by(phone=phone).first()
    if not result:
        return None
    return result

def verify_manage_destroy(id):
    session = get_session()
    with session.begin():
        query = model_query(models.VerifyManage, session=session, id=id)
        query.delete(synchronize_session=False)

#################verify manage end#######################################