#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy import orm

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
        sessionmaker = orm.get_maker(engine=engine, autocommit=autocommit)
        return sessionmaker
        #sessionmaker(bind=engine, autocommit=autocommit)