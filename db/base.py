#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import object_mapper
import simplejson
import six
from datetime import datetime
import threading
from util.ini_client import ini_load
from enginefacade import EngineFacade

_conf = ini_load('config/mysql.ini')
_dic_con = _conf.get_fields('product_db')

connect = 'mysql://{0}:{1}@{2}:{3}/{4}?charset=utf8'.format(
    _dic_con.get('user'),
    _dic_con.get('password'),
    _dic_con.get('host'),
    _dic_con.get('port', 3306),
    _dic_con.get('database')
)

_LOCK = threading.Lock()
_FACADE = None


def _create_facade_lazily():
    global _LOCK
    with _LOCK:
        global _FACADE
        if _FACADE is None:
            args = {
                "encoding": "utf8",
                "convert_unicode": True
            }
            _FACADE = EngineFacade(connect, **args)

        return _FACADE

def get_engine():
    facade = _create_facade_lazily()
    return facade.get_engine()


def get_session():
    facade = _create_facade_lazily()
    return facade.get_session()


class ModelBase(six.Iterator):
    """Base class for models."""
    __table_initialized__ = False

    def save(self, session):
        """Save this object."""
        with session.begin(subtransactions=True):
            session.add(self)
            session.flush()

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)

    def __contains__(self, key):
        try:
            getattr(self, key)
        except AttributeError:
            return False
        else:
            return True

    def get(self, key, default=None):
        return getattr(self, key, default)

    @property
    def _extra_keys(self):
        return []

    def __iter__(self):
        columns = list(dict(object_mapper(self).columns).keys())
        # NOTE(russellb): Allow models to specify other keys that can be looked
        # up, beyond the actual db columns.  An example would be the 'name'
        # property for an Instance.
        columns.extend(self._extra_keys)

        return ModelIterator(self, iter(columns))

    def update(self, values):
        """Make the model object behave like a dict."""
        for k, v in six.iteritems(values):
            setattr(self, k, v)

    def _as_dict(self):
        """Make the model object behave like a dict.

        Includes attributes from joins.
        """
        local = dict((key, value) for key, value in self)
        joined = dict([(k, v) for k, v in six.iteritems(self.__dict__)
                      if not k[0] == '_'])
        local.update(joined)
        return local

    def iteritems(self):
        """Make the model object behave like a dict."""
        return six.iteritems(self._as_dict())

    def items(self):
        """Make the model object behave like a dict."""
        return self._as_dict().items()

    def keys(self):
        """Make the model object behave like a dict."""
        return [key for key, value in self.iteritems()]

class ModelIterator(six.Iterator):

    def __init__(self, model, columns):
        self.model = model
        self.i = columns

    def __iter__(self):
        return self

    # In Python 3, __next__() has replaced next().
    def __next__(self):
        n = six.advance_iterator(self.i)
        return n, getattr(self.model, n)

class DateJsonEncoder(simplejson.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.__str__()
        return simplejson.JSONEncoder.default(self, obj)

class AlchemyEncoder(simplejson.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                try:
                    data = unicode(obj.__getattribute__(field))
                    simplejson.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except Exception:
                    fields[field] = None
            # a json-encodable dict
            return fields

        if isinstance(obj, datetime):
            return obj.__str__()
        return simplejson.JSONEncoder.default(self, obj)

def json_dumps_time(json,**kwargs):
    """
    获取json串，带time
    :param json:
    :param kwargs:
    :return:
    """
    return simplejson.dumps(json,cls=DateJsonEncoder, **kwargs)

def json_dumps_alchemy(json,**kwargs):
    return simplejson.dumps(json, cls=AlchemyEncoder, **kwargs)

def json_load(str_json):
    return simplejson.loads(str_json)