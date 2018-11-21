#!/usr/bin/python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Table, MetaData, UniqueConstraint, ForeignKey

from sqlalchemy.types import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from base import get_engine, ModelBase

Base = declarative_base()

def _to_dict(model_obj):
    result = {}
    for c in model_obj.__table__.columns:
        if isinstance(getattr(model_obj, c.name, None), datetime):
            if c.name == "birthday":
                result.update({c.name: getattr(model_obj, c.name, None).strftime('%Y-%m-%d')})
            else:
                result.update({c.name: getattr(model_obj, c.name, None).strftime('%Y-%m-%d %H:%M:%S')})
        else:
            result.update({c.name: getattr(model_obj, c.name, None)})
    return result


class SchoolInfo(Base, ModelBase):
    __tablename__ = 'school_info'
    id = Column(VARCHAR(36), primary_key=True)
    name = Column(VARCHAR(100), nullable=False)
    cardcode = Column(VARCHAR(36))
    describe = Column(VARCHAR(500))
    faceset_token = Column(VARCHAR(36))
    deleted = Column(Boolean, default=False)
    create_time = Column(DateTime, default=datetime.now, nullable=False)
    updated_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return _to_dict(self)
       #return {c.name: getattr(self, c.name, None).strftime('%Y-%m-%d %H:%M:%S') if isinstance(getattr(self, c.name, None), datetime) else getattr(self, c.name, None) for c in self.__table__.columns}

class GradeInfo(Base, ModelBase):
    __tablename__ = 'grade_info'
    id = Column(VARCHAR(36), primary_key=True)
    name = Column(VARCHAR(100), nullable=False)
    school_id = Column(VARCHAR(36), ForeignKey("school_info.id"))
    deleted = Column(Boolean, default=False)
    create_time = Column(DateTime, default=datetime.now, nullable=False)
    updated_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return _to_dict(self)
       #return {c.name: getattr(self, c.name, None).strftime('%Y-%m-%d %H:%M:%S') if isinstance(getattr(self, c.name, None), datetime) else getattr(self, c.name, None) for c in self.__table__.columns}


class ClassInfo(Base, ModelBase):
    __tablename__ = 'class_info'
    id = Column(VARCHAR(36), primary_key=True)
    name = Column(VARCHAR(100), nullable=False)
    grade_id = Column(VARCHAR(36), ForeignKey("grade_info.id"))
    cardcode = Column(VARCHAR(36), nullable=False)
    school_id = Column(VARCHAR(36), ForeignKey("school_info.id"))
    student_number = Column(Integer, default=0)
    describe = Column(VARCHAR(500))
    deleted = Column(Boolean, default=False)
    create_time = Column(DateTime, default=datetime.now, nullable=False)
    updated_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return _to_dict(self)
       #return {c.name: getattr(self, c.name, None).strftime('%Y-%m-%d %H:%M:%S') if isinstance(getattr(self, c.name, None), datetime) else getattr(self, c.name, None) for c in self.__table__.columns}

class TeacherInfo(Base, ModelBase):
    __tablename__ = 'teacher_info'
    id = Column(VARCHAR(36), primary_key=True)
    name = Column(VARCHAR(100), nullable=False)
    sex = Column(Integer, default=0)
    birthday = Column(DateTime)
    school_id = Column(VARCHAR(36), ForeignKey("school_info.id"))
    grade_id = Column(VARCHAR(36), ForeignKey("grade_info.id"))
    class_id = Column(VARCHAR(500))
    user_id = Column(VARCHAR(36))
    phone = Column(VARCHAR(36))
    position = Column(Integer, default=2)
    describe = Column(VARCHAR(500))
    deleted = Column(Boolean, default=False)
    create_time = Column(DateTime, default=datetime.now, nullable=False)
    updated_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return _to_dict(self)
       #return {c.name: getattr(self, c.name, None).strftime('%Y-%m-%d %H:%M:%S') if isinstance(getattr(self, c.name, None), datetime) else getattr(self, c.name, None) for c in self.__table__.columns}

class TeacherHistory(Base, ModelBase):
    __tablename__ = 'teacher_history'
    id = Column(VARCHAR(36), primary_key=True)
    teacher_id = Column(VARCHAR(36), nullable=False)
    status = Column(VARCHAR(36), default="education")
    describe = Column(VARCHAR(500))
    deleted = Column(Boolean, default=False)
    create_time = Column(DateTime, default=datetime.now, nullable=False)
    updated_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return _to_dict(self)
       #return {c.name: getattr(self, c.name, None).strftime('%Y-%m-%d %H:%M:%S') if isinstance(getattr(self, c.name, None), datetime) else getattr(self, c.name, None) for c in self.__table__.columns}


class StudentInfo(Base, ModelBase):
    __tablename__ = 'student_info'
    id = Column(VARCHAR(36), primary_key=True)
    name = Column(VARCHAR(100), nullable=False)
    sex = Column(Integer, default=0)
    birthday = Column(DateTime)
    school_id = Column(VARCHAR(36), nullable=False)
    grade_id = Column(VARCHAR(36), nullable=False)
    class_id = Column(VARCHAR(36), nullable=False)
    user_id = Column(VARCHAR(36))
    relation_number = Column(Integer, default=3)
    describe = Column(VARCHAR(500))
    deleted = Column(Boolean, default=False)
    create_time = Column(DateTime, default=datetime.now, nullable=False)
    updated_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return _to_dict(self)
       #return {c.name: getattr(self, c.name, None).strftime('%Y-%m-%d %H:%M:%S') if isinstance(getattr(self, c.name, None), datetime) else getattr(self, c.name, None) for c in self.__table__.columns}

class StudentHistory(Base, ModelBase):
    __tablename__ = 'student_history'
    id = Column(VARCHAR(36), primary_key=True)
    student_id = Column(VARCHAR(36), nullable=False)
    status = Column(VARCHAR(36), default="apply")
    describe = Column(VARCHAR(500))
    deleted = Column(Boolean, default=False)
    create_time = Column(DateTime, default=datetime.now, nullable=False)
    updated_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return _to_dict(self)
       #return {c.name: getattr(self, c.name, None).strftime('%Y-%m-%d %H:%M:%S') if isinstance(getattr(self, c.name, None), datetime) else getattr(self, c.name, None) for c in self.__table__.columns}

class RelativeInfo(Base, ModelBase):
    __tablename__ = 'relative_info'
    id = Column(VARCHAR(36), primary_key=True)
    name = Column(VARCHAR(100), nullable=False)
    sex = Column(Integer, default=0)
    birthday = Column(DateTime)
    user_id = Column(VARCHAR(36))
    wxuser_id = Column(VARCHAR(36))
    phone = Column(VARCHAR(36), nullable=False)
    describe = Column(VARCHAR(500))
    #face_token = Column(VARCHAR(36))
    deleted = Column(Boolean, default=False)
    create_time = Column(DateTime, default=datetime.now, nullable=False)
    updated_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return _to_dict(self)
       #return {c.name: getattr(self, c.name, None).strftime('%Y-%m-%d %H:%M:%S') if isinstance(getattr(self, c.name, None), datetime) else getattr(self, c.name, None) for c in self.__table__.columns}

class RelevanceFace(Base, ModelBase):
    __tablename__ = 'relevance_face'
    id = Column(VARCHAR(36), primary_key=True)
    school_id = Column(VARCHAR(36), nullable=False)
    relevance_id = Column(VARCHAR(36), nullable=False)
    relevance_type = Column(Integer, default=1)
    face_token = Column(VARCHAR(36), nullable=False)
    faceset_token = Column(VARCHAR(36), nullable=False)
    deleted = Column(Boolean, default=False)
    create_time = Column(DateTime, default=datetime.now, nullable=False)
    updated_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return _to_dict(self)
       #return {c.name: getattr(self, c.name, None).strftime('%Y-%m-%d %H:%M:%S') if isinstance(getattr(self, c.name, None), datetime) else getattr(self, c.name, None) for c in self.__table__.columns}


class RelationInfo(Base, ModelBase):
    __tablename__ = 'relation_info'
    id = Column(VARCHAR(36), primary_key=True)
    relation = Column(VARCHAR(36), nullable=False)
    student_id = Column(VARCHAR(36), nullable=False)
    relative_id = Column(VARCHAR(36), nullable=False)
    deleted = Column(Boolean, default=False)
    create_time = Column(DateTime, default=datetime.now, nullable=False)
    updated_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    UniqueConstraint('student_id', 'relative_id')

    def to_dict(self):
        return _to_dict(self)
       #return {c.name: getattr(self, c.name, None).strftime('%Y-%m-%d %H:%M:%S') if isinstance(getattr(self, c.name, None), datetime) else getattr(self, c.name, None) for c in self.__table__.columns}

class UserInfo(Base, ModelBase):
    __tablename__ = 'user_info'
    id = Column(VARCHAR(36), primary_key=True)
    name = Column(VARCHAR(100), nullable=False)
    pwd = Column(VARCHAR(100), nullable=False)
    verify_code = Column(VARCHAR(100))
    activate = Column(Integer, default=0)
    level = Column(Integer, default=1)
    deleted = Column(Boolean, default=False)
    create_time = Column(DateTime, default=datetime.now, nullable=False)
    updated_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return _to_dict(self)
       #return {c.name: getattr(self, c.name, None).strftime('%Y-%m-%d %H:%M:%S') if isinstance(getattr(self, c.name, None), datetime) else getattr(self, c.name, None) for c in self.__table__.columns}


class WXUserInfo(Base, ModelBase):
    __tablename__ = 'wx_userinfo'
    id = Column(VARCHAR(36), primary_key=True)
    openid = Column(VARCHAR(50), nullable=False)
    session_key = Column(VARCHAR(50), nullable=False)
    phone = Column(VARCHAR(36))
    deleted = Column(Boolean, default=False)
    create_time = Column(DateTime, default=datetime.now, nullable=False)
    updated_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return _to_dict(self)
       #return {c.name: getattr(self, c.name, None).strftime('%Y-%m-%d %H:%M:%S') if isinstance(getattr(self, c.name, None), datetime) else getattr(self, c.name, None) for c in self.__table__.columns}


class RelativeSignInfo(Base, ModelBase):
    __tablename__ = 'relative_sign_info'
    id = Column(VARCHAR(36), primary_key=True)
    relative_id = Column(VARCHAR(36), nullable=False)
    create_time = Column(DateTime, default=datetime.now, nullable=False)
    type = Column(Integer, default=0)
    deleted = Column(Boolean, default=False)

    def to_dict(self):
        return _to_dict(self)
        """
        return {
        c.name: getattr(self, c.name, None).strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(getattr(self, c.name, None),
                      datetime) else getattr(self, c.name, None)
        for c in self.__table__.columns}
        """


class TeacherSignInfo(Base, ModelBase):
    __tablename__ = 'teacher_sign_info'
    id = Column(VARCHAR(36), primary_key=True)
    teacher_id = Column(VARCHAR(36), nullable=False)
    create_time = Column(DateTime, default=datetime.now, nullable=False)
    type = Column(Integer, default=0)
    deleted = Column(Boolean, default=False)

    def to_dict(self):
        return _to_dict(self)
        """
        return {
        c.name: getattr(self, c.name, None).strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(getattr(self, c.name, None),
                      datetime) else getattr(self, c.name, None)
        for c in self.__table__.columns}
        """

class VerifyManage(Base, ModelBase):
    __tablename__ = 'verify_manage'
    id = Column(VARCHAR(36), primary_key=True)
    phone = Column(VARCHAR(36))
    email = Column(VARCHAR(36))
    verify_code = Column(VARCHAR(36))
    updated_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    def to_dict(self):
        return _to_dict(self)

def register_db():
    engine = get_engine()
    Base.metadata.create_all(engine)


def unregister_db():
    engine = get_engine()
    Base.metadata.drop_all(engine)