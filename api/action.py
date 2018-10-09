#coding:utf-8

from tornado.web import RequestHandler
import json
import urllib
import re
import uuid
import tempfile
import Image
from util.convert import is_mobile
import logging

LOG = logging.getLogger(__name__)
MIN_FILE_SIZE = 1 #bytes
MAX_FILE_SIZE = 5000000 #bytes
IMAGE_TYPES = re.compile('image/(gif|p?jpeg|(x-)?png)')
ACCEPT_FILE_TYPES = IMAGE_TYPES

class ActionHandler(RequestHandler):
    def validate(self, file):
        if file['size'] < MIN_FILE_SIZE:
            file['error'] = 'File is too small'
        elif file['size'] > MAX_FILE_SIZE:
            file['error'] = 'File is too big'
        elif not ACCEPT_FILE_TYPES.match(file['type']):
            file['error'] = 'Filetype not allowed'
        else:
            return True
        return False

    # 待处理
    def write_blob(self, tf, info):
        img = Image.open(tf.name)
        img.thumbnail((920, 920), resample=1)
        #图片写到本地
        img.save(self.application.settings.get('static_path') + '/uploadimage/' + info["dstname"])
        #写到数据库
        return info["dstname"]

    def handle_upload(self):
        results = []
        blob_keys = []
        for name in self.request.files:
            fieldStorage=self.request.files.get(name)
            if type(fieldStorage) is unicode:
                continue
            result = {}
            result['name'] = re.sub(r'^.*\\', '', fieldStorage[0]['filename'])
            result['dstname'] = str(uuid.uuid1())+'.'+result['name'].split('.').pop()#存储在服务的图片名
            result['thbname'] = "thumb_"+result['dstname']#缩略图
            result['type'] = fieldStorage[0]['content_type']
            tf = tempfile.NamedTemporaryFile()
            tf.write(fieldStorage[0]['body'])
            result['size'] = self.get_file_size(tf)
            if self.validate(result):
                blob_key = str(self.write_blob(tf, result))
                blob_keys.append(blob_key)
                result['deleteType'] = 'DELETE'
                result['deleteUrl'] = self.request.host+'/?key='+urllib.quote(blob_key, '')
                #result['deleteUrl'] = self.request.host_url+'/?key='+urllib.quote(blob_key,'')
                if(IMAGE_TYPES.match(result['type'])):
                    try:#待处理
                        pass
                    except:
                        pass
                if not 'url' in result:
                    result['url'] = "https://"+self.request.host+'/upload_img/'+blob_key
            results.append(result)

        return results

    def post(self, action):
        if action == "identy":
            relative_code = self.get_argument('relative_code', '')
            file = self.handle_upload()
            pass
        if action == "signin":
            cardcode = self.get_argument('cardcode', '')

            pass
        if action == "signout":
            cardcode = self.get_argument('cardcode', '')
            pass