#coding:utf-8

import logging
from util.ini_client import ini_load
import requests
from util.face_recognition_api import Face_Recognition_YYL

LOG = logging.getLogger(__name__)

_conf = ini_load('config/service.ini')
_dic_con = _conf.get_fields('face++')
face_api_key = _dic_con.get("api_key", "")
face_api_secret = _dic_con.get("api_secret", "")
face_create_url = _dic_con.get("create_url", "")
face_detect_url = _dic_con.get("detect_url", "")
face_add_url    = _dic_con.get("add_url","")
face_remove_url = _dic_con.get("remove_url","")

face_recognition_yyl = Face_Recognition_YYL(face_api_key, face_api_secret, face_create_url, face_detect_url, \
                                    face_add_url,face_remove_url, '', '', '', '')

'''
描述：人脸库创建
参数：school_name：学校名称；school_id：学校id
返回：返回码和数据信息，正确情况：code=200；错误情况：code=其它数，见错误码类型
同时将results值更新至表school_info字段faceset_token
'''
code , results = face_recognition_yyl.FaceSet_Create(school_name, school_id)

'''
描述：人脸检测
参数：file_path：图片路径
返回：返回码和数据信息，正确情况：code=200；错误情况：code=其它数，见错误码类型
同时保存results值(对应face_tokens值)
'''
code,results = face_recognition_yyl.Face_Detect(file_path)
'''
描述：人脸添加
参数：school_id：学校id,face_tokens：Face_Detect返回得face_tokens
返回：返回码和数据信息，正确情况：code=200；错误情况：code=其它数，见错误码类型
将人脸检测获取得face_tokens，写入表relative_info的face_token
'''
code,results = face_recognition_yyl.Face_Add(school_id,face_tokens)

'''
描述：人脸删除
参数：school_id：学校id,face_tokens：face_tokens
返回：返回码和数据信息，正确情况：code=200；错误情况：code=其它数，见错误码类型
获取school_id和face_tokens 删除人脸
'''
code,results = face_recognition_yyl.Face_Remove(school_id,face_tokens)

#
# def face_identy(file_path):
#     """
#     通过第三方api获取人脸特征
#     :param file_path: 图片路径
#     :return:
#     """
#     _file = open(file_path, 'rb').read()
#     files = {'image_file': _file}
#     # 人脸检测
#     data = {
#         'api_key': face_api_key,
#         'api_secret': face_api_secret,
#     }
#     response = requests.post(face_detect_url, data=data, files=files)
#     results = response.json()
#     if results.get('error_message'):
#         LOG.info("face++ identy error:%s"%results.get('error_message'))
#         return 1, results.get('error_message')
#
#     face_token = results['faces'][-1]['face_token']
#     return 0, face_token
#
# def create_face_tokenset(school_obj):
#     # 人脸库创建
#     data = {
#         'api_key': face_api_key,
#         'api_secret': face_api_secret,
#         'display_name': school_obj.get("name"),
#         'outer_id': school_obj.get("id"),
#         'tags': school_obj.get("id"),
#     }
#     response = requests.post(face_create_url, data)
#     results = response.json()
#     if results.get('error_message', ""):
#         LOG.error("create face tokenset error:%s" % results.get('error_message'))
#         return
#
#     faceset_token = results.get('faceset_token', "")  # faceset
#     return faceset_token