#coding:utf-8

import logging
from util.ini_client import ini_load
import requests

LOG = logging.getLogger(__name__)

_conf = ini_load('config/service.ini')
_dic_con = _conf.get_fields('face++')
face_api_key = _dic_con.get("api_key", "")
face_api_secret = _dic_con.get("api_secret", "")
face_create_url = _dic_con.get("create_url", "")
face_detect_url = _dic_con.get("detect_url", "")


def face_identy(file_path):
    """
    通过第三方api获取人脸特征
    :param file_path: 图片路径
    :return:
    """
    _file = open(file_path, 'rb').read()
    files = {'image_file': _file}
    # 人脸检测
    data = {
        'api_key': face_api_key,
        'api_secret': face_api_secret,
    }
    response = requests.post(face_detect_url, data=data, files=files)
    results = response.json()
    if results.get('error_message'):
        LOG.info("face++ identy error:%s"%results.get('error_message'))
        return 1, results.get('error_message')

    face_token = results['faces'][-1]['face_token']
    return 0, face_token

def create_face_tokenset(school_obj):
    # 人脸库创建
    data = {
        'api_key': face_api_key,
        'api_secret': face_api_secret,
        'display_name': school_obj.get("name"),
        'outer_id': school_obj.get("id"),
        'tags': school_obj.get("id"),
    }
    response = requests.post(face_create_url, data)
    results = response.json()
    if results.get('error_message', ""):
        LOG.error("create face tokenset error:%s" % results.get('error_message'))
        return

    faceset_token = results.get('faceset_token', "")  # faceset
    return faceset_token