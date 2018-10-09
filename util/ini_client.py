#!/usr/bin/python
# -*- coding: UTF-8 -*-
from ConfigParser import ConfigParser
import re
from functools import partial
from os import path

user_pat=re.compile(r'~')
#只支持_或者ascii字母开头的变量
var_pat=re.compile(r'\$(?P<name>[_a-zA-Z][_\-a-zA-Z\d]*)')
curuser=path.expanduser(user_pat.pattern)

def _match_user(m):
    #扩展~到当前用户
    return curuser

def reg_sub_ex(reg_ob,s,mcb):
    assert mcb and callable(mcb)

    ms=tuple(reg_ob.finditer(s))
    if not ms:
        return  s

    rt = []
    for i in xrange(len(ms)):
        unmatch=s[0:ms[i].start()] if i==0 else s[ms[i-1].end():ms[i].start()]
        rt.append(unmatch)
        rt.append(mcb(ms[i]))

    rt.append(s[ms[-1].end():])
    return ''.join(rt)

class Config_INI(object):
    def __init__(self,cfg_fn):
        assert cfg_fn and path.isfile(cfg_fn),'{0} not existed!'.format(cfg_fn)

        self.__type_map={
            int:'int',
            bool:'boolean',
            float:'float'
        }
        self.__config=ConfigParser()
        self.__config.read(cfg_fn)

        self.__cache={}
        for s in self.get_sections():
            if s not in self.__cache:
                self.__cache.update({s:{}})
            for f in self.get_fields(s):
                self.__cache[s].update({f:self.get(s,f)})


    def __match_field(self,m,dest_key=None):
        """
        匹配以后的建值
        """
        key=m.groupdict().get("name")
        if dest_key and key == dest_key:
            raise ValueError('recersion key %r'%key)

        for v in self.__cache.itervalues():
            if key not in v:
                continue
            return v.get(key)
        raise ValueError('key %r ot found'%key)

    def get_resolve(self, section, key):
        """
        对于$开头的字符串，会解引用
        对于~字符，解析到当前用户目录
        """
        v = self.get(section, key)
        if v is None:
            return v
        match_raw_dest = partial(self.__match_field, dest_key=key)
        _sub_ex0=reg_sub_ex(var_pat, v, match_raw_dest)
        return reg_sub_ex(user_pat, _sub_ex0, _match_user)

    def get(self, section, key, _type=None):
        """获取seciton对应key的value

        section: ini文件section name
        key: ini文件key name
        _type: value需要转换的类型
            None: basestring
            int: int
            bool: boolean
            float: float
        """
        if not section or not key:
            return None
        if not isinstance(section, basestring):
            return None
        if not isinstance(key, basestring):
            return None

        if not self.__config.has_option(section, key):
            return None

        if not _type or _type not in self.__type_map:
            return self.__config.get(section, key)

        mtd = getattr(self.__config, 'get{0}'.format(self.__type_map.get(_type)))
        return mtd(section, key)

    def get_fields(self, section):
        if not section:
            return {}
        if not isinstance(section, basestring):
            return {}
        if not self.__config.has_section(section):
            return {}
        return dict(self.__config.items(section))

    def has_section(self, section):
        if not section:
            return False
        if not isinstance(section, basestring):
            return False
        return self.__config.has_section(section)

    def get_sections(self):
        return self.__config.sections()


ini_load = Config_INI

