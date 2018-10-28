#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
import sqlalchemy.orm
from sqlalchemy.sql.expression import literal_column
from datetime import datetime
import threading
import update_match

class Query(sqlalchemy.orm.query.Query):
    """Subclass of sqlalchemy.query with soft_delete() method."""
    def soft_delete(self, synchronize_session='evaluate'):
        return self.update({'deleted': literal_column('id'),
                            'updated_at': literal_column('updated_at'),
                            'deleted_at': datetime.utcnow()},
                           synchronize_session=synchronize_session)

    def update_returning_pk(self, values, surrogate_key):
        """Perform an UPDATE, returning the primary key of the matched row.

        This is a method-version of
        oslo_db.sqlalchemy.update_match.update_returning_pk(); see that
        function for usage details.

        """
        return update_match.update_returning_pk(self, values, surrogate_key)

    def update_on_match(self, specimen, surrogate_key, values, **kw):
        """Emit an UPDATE statement matching the given specimen.

        This is a method-version of
        oslo_db.sqlalchemy.update_match.update_on_match(); see that function
        for usage details.

        """
        return update_match.update_on_match(
            self, specimen, surrogate_key, values, **kw)

class Session(sqlalchemy.orm.session.Session):
    """oslo.db-specific Session subclass."""

class EngineFacade():
    def __init__(self, connect, **kwargs):
        self.connect = connect
        self.kwargs = kwargs
        self._start_lock = threading.Lock()
        self._started = False
        self._start(self.connect)

    def get_engine(self, connect=""):
        connect = connect or self.connect
        engine = create_engine(connect, **self.kwargs)
        return engine

    def get_session(self,  **kwargs):
        return self._maker(**kwargs)

    def _setup_for_connection(self, connect="", autocommit=True):
        connect = connect or self.connect
        engine = create_engine(connect, **self.kwargs)
        sessionmaker = sqlalchemy.orm.sessionmaker(bind=engine,
                                                   class_=Session,
                                                   autocommit=autocommit,
                                                   query_cls=Query)
        return engine, sessionmaker

    def _start(self, connect="",):
        with self._start_lock:
            if self._started:
                return

            self._engine, self._maker = \
                self._setup_for_connection(connect=connect)

            self._started = True