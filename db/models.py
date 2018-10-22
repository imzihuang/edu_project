#!/usr/bin/python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Table, MetaData

from sqlalchemy.types import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from base import get_engine

BaseModel = declarative_base()

class SchoolInfo(BaseModel):
    __tablename__ = 'school_info'
    id = Column(VARCHAR(36), primary_key=True)
    name = Column(VARCHAR(100), nullable=False)
    cardcode = Column(VARCHAR(36), nullable=False)
    describe = Column(VARCHAR(500), nullable=False)
    create_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_time = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
       return {c.name: getattr(self, c.name, None).strftime('%Y-%m-%d %H:%M:%S') if isinstance(getattr(self, c.name, None), datetime) else getattr(self, c.name, None) for c in self.__table__.columns}

class ClassInfo(BaseModel):
    __tablename__ = 'class_info'
    id = Column(VARCHAR(36), primary_key=True)
    name = Column(VARCHAR(100), nullable=False)
    grade = Column(VARCHAR(100))
    school_id = Column(VARCHAR(36), nullable=False)
    student_number = Column(Integer, default=0)
    create_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_time = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
       return {c.name: getattr(self, c.name, None).strftime('%Y-%m-%d %H:%M:%S') if isinstance(getattr(self, c.name, None), datetime) else getattr(self, c.name, None) for c in self.__table__.columns}

class TeacherInfo(BaseModel):
    __tablename__ = 'teacher_info'
    id = Column(VARCHAR(36), primary_key=True)
    name = Column(VARCHAR(100), nullable=False)
    sex = Column(Integer, default=0)
    age = Column(Integer, default=1)
    school_id = Column(VARCHAR(36), nullable=False)
    class_id = Column(VARCHAR(36), nullable=False)
    user_id = Column(VARCHAR(36), nullable=False)
    create_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_time = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
       return {c.name: getattr(self, c.name, None).strftime('%Y-%m-%d %H:%M:%S') if isinstance(getattr(self, c.name, None), datetime) else getattr(self, c.name, None) for c in self.__table__.columns}

class StudentInfo(BaseModel):
    __tablename__ = 'student_info'
    id = Column(VARCHAR(36), primary_key=True)
    name = Column(VARCHAR(100), nullable=False)
    sex = Column(Integer, default=0)
    age = Column(Integer, default=1)
    school_id = Column(VARCHAR(36), nullable=False)
    class_id = Column(VARCHAR(36), nullable=False)
    status = Column(VARCHAR(36), default="apply")
    user_id = Column(VARCHAR(36), nullable=False)
    relation_number = Column(Integer, default=3)
    create_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_time = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
       return {c.name: getattr(self, c.name, None).strftime('%Y-%m-%d %H:%M:%S') if isinstance(getattr(self, c.name, None), datetime) else getattr(self, c.name, None) for c in self.__table__.columns}

class RelativeInfo(BaseModel):
    __tablename__ = 'relative_info'
    id = Column(VARCHAR(36), primary_key=True)
    name = Column(VARCHAR(100), nullable=False)
    sex = Column(Integer, default=0)
    age = Column(Integer, default=1)
    student_id = Column(VARCHAR(200), nullable=False)
    user_id = Column(VARCHAR(36), nullable=False)
    relation = Column(VARCHAR(36), nullable=False)
    phone = Column(VARCHAR(36), nullable=False)

    create_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_time = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
       return {c.name: getattr(self, c.name, None).strftime('%Y-%m-%d %H:%M:%S') if isinstance(getattr(self, c.name, None), datetime) else getattr(self, c.name, None) for c in self.__table__.columns}

class RelativeFeature(BaseModel):
    __tablename__ = 'relative_feature'
    id = Column(VARCHAR(36), primary_key=True)
    relative_id = Column(VARCHAR(36), nullable=False)
    features = Column(LargeBinary(length=65536))

class UserInfo(BaseModel):
    __tablename__ = 'user_info'
    id = Column(VARCHAR(36), primary_key=True)
    name = Column(VARCHAR(100), nullable=False)
    pwd = Column(VARCHAR(100), nullable=False)
    verify_code = Column(VARCHAR(100))
    activate = Column(Integer, default=0)
    level = Column(Integer, default=1)

    def to_dict(self):
       return {c.name: getattr(self, c.name, None).strftime('%Y-%m-%d %H:%M:%S') if isinstance(getattr(self, c.name, None), datetime) else getattr(self, c.name, None) for c in self.__table__.columns}


class SignInfo(BaseModel):
    __tablename__ = 'sign_info'
    id = Column(VARCHAR(36), primary_key=True)
    relative_id = Column(VARCHAR(36), nullable=False)
    relative_name = Column(VARCHAR(100), nullable=False)
    create_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    type = Column(Integer, default=0)

    def to_dict(self):
        return {
        c.name: getattr(self, c.name, None).strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(getattr(self, c.name, None),
                      datetime) else getattr(self, c.name, None)
        for c in self.__table__.columns}


def register_db():
    engine = get_engine()
    BaseModel.metadata.create_all(engine)


def unregister_db():
    engine = get_engine()
    BaseModel.metadata.drop_all(engine)