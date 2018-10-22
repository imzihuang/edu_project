#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class Session(sqlalchemy.orm.session.Session):
    """oslo.db-specific Session subclass."""

class EngineFacade():
    def __init__(self, connect, **kwargs):
        self.connect = connect
        self.kwargs = kwargs

    def get_engine(self, connect=""):
        connect = connect or self.connect
        engine = create_engine(connect, **self.kwargs)
        return engine

    def get_session(self, connect="", autocommit=True):
        connect = connect or self.connect
        engine = create_engine(connect, **self.kwargs)
        return sessionmaker(bind=engine,
                            class_=Session,
                            autocommit=autocommit,
                            expire_on_commit=False)