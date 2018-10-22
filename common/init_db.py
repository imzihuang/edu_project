# coding:utf-8

from db.models import register_db
from db import api
from util.encrypt_md5 import encry_md5

def add_user(admin_userinfo):
    try:
        api.user_create(admin_userinfo)
        return True
    except Exception as ex:
        raise ex

#先创建好数据库
#CREATE DATABASE `eduprodb` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

if __name__ == "__main__":
    register_db()
    add_user({
        "name": "admin",
        "pwd": encry_md5("ewixqqssssss3$#@s"),
        "activate": 1,
        "level": 0
    })

