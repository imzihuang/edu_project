# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 14:24:21 2018
@author: chenlonghua
https://console.faceplusplus.com.cn/documents/5671787
函数功能描述：
FaceSet_Create：创建一个人脸的集合 FaceSet，用于存储人脸标识 face_token。一个 FaceSet 能够存储 10000 个 face_token
FaceSet_Delete：删除一个人脸集合
FaceSet_Get：获取一个 FaceSet 的所有信息，包括此 FaceSet 的 faceset_token, outer_id, display_name 的信息，
FaceSet_GetFS：获取某一 API Key 下的 FaceSet 列表及其 faceset_token、outer_id、display_name 和 tags 等信息
Face_Detect：传入图片进行人脸检测和人脸分析。检测图片内的所有人脸，对于每个检测出的人脸，会给出其唯一标识 face_token
Face_Add：为一个已经创建的 FaceSet 添加人脸标识 face_token。一个 FaceSet 最多存储10000个 face_token。
Face_Remove：移除一个FaceSet中的某些或者全部face_token
Face_Search:在一个已有的 FaceSet 中找出与目标人脸最相似的一张或多张人脸，返回置信度和不同误识率下的阈值。
"""

import os 
from PIL import Image 
import requests 

class Face_Recognition(object):
    
    def __init__(self,api_key,api_secret,create_url,detect_url,\
                 add_url,search_url,delete_url,get_url,get_fs_url,remove_url):
        self.api_key = api_key 
        self.api_secret= api_secret 
        self.create_url = create_url 
        self.detect_url = detect_url 
        self.add_url = add_url
        self.search_url = search_url
        self.delete_url = delete_url
        self.get_url = get_url
        self.get_fs_url = get_fs_url
        self.remove_url = remove_url
    
    #人脸库创建
    def FaceSet_Create(self,display_name,outer_id,tags):   
        data = {
                'api_key':self.api_key,
                'api_secret':self.api_secret,
                'display_name':display_name, #对应学校名称
                'outer_id':outer_id, #对应学校id
                'tags':tags,  #对应学校id
                }
        response = requests.post(self.create_url,data=data)
        if response.status_code ==200:
            results = response.json()
            faceset_token = results['faceset_token']  #返回人脸库的faceset_token，唯一码
            return response.status_code,faceset_token
        return response.status_code,response.json() #返回错误码和报错信息

    #删除人脸库
    def FaceSet_Delete(self,outer_id):
        data = {
                'api_key':self.api_key,
                'api_secret':self.api_secret,
                'outer_id':outer_id, #对应学校id
                #'faceset_token':faceset_token
                }
        response = requests.post(self.delete_url,data=data)
        if response.status_code ==200:
            results = response.json()
            faceset_token = results['faceset_token']  #返回人脸库的faceset_token，唯一码
            return response.status_code,faceset_token
        return response.status_code,response.json() #返回错误码和报错信息

    #获取人脸库信息
    def FaceSet_Get(self,outer_id):
        data = {
                'api_key':self.api_key,
                'api_secret':self.api_secret,
                 'outer_id':outer_id, #对应学校id
                #'faceset_token':faceset_token
                }
        response = requests.post(self.get_url,data=data)
        if response.status_code ==200:
            results = response.json()
            return response.status_code,results
        return response.status_code,response.json()

    #获取API Key下所有人脸库
    def FaceSet_GetFS(self):
        data = {
                'api_key':self.api_key,
                'api_secret':self.api_secret,
                }
        response = requests.post(self.get_fs_url,data=data)
        if response.status_code ==200:
            results = response.json()
            return response.status_code,results
        return response.status_code,response.json()

    #Face++ 接口要求传入的图片大小不能2M的图片
    def img_resize(self, path):
        fsize = os.path.getsize(path)
        s = 1920 
        if fsize <= 2097152: #判断是否大于2M
            return
        if path[-3:] in ['png','PNG']: #区分png和jpg，png图片大
            s = 960
        ims = Image.open(path)
        w = ims.width / s
        h = ims.height / s
        if w > h:
            width = s
            height = int(s * (h / w))
        else:
            height = s
            width = int(s * (w / h))
    
        ims = ims.resize((width, height))
        ims.save(path)

    #人脸检测
    def Face_Detect(self,image_path):
        self.img_resize(image_path)
        files = {'image_file':open(image_path,'rb').read()}
        data = {
            'api_key':self.api_key,
            'api_secret':self.api_secret,
        }
        response = requests.post(self.detect_url,data=data,files=files)
        if response.status_code ==200:
            results = response.json()
            if results['faces']:
                face_token = results['faces'][0]['face_token'] #返回人脸的face_token,唯一码
                return response.status_code,face_token
            else:
                return response.status_code,None  #检测不到人脸
        return response.status_code,response.json() #返回错误码和报错信息
    
    #添加人脸
    def Face_Add(self,outer_id,face_tokens):
        data = {
            'api_key':self.api_key,
            'api_secret':self.api_secret,
            'outer_id':outer_id ,
            'face_tokens':face_tokens
        }
        response = requests.post(self.add_url,data=data )
        if response.status_code ==200:
            results = response.json()
            return response.status_code,results
        return response,response.json()

    #删除人脸
    def Face_Remove(self,outer_id,face_tokens):
        data = {
            'api_key':self.api_key,
            'api_secret':self.api_secret,
            'outer_id':outer_id ,
            #'faceset_token':faceset_token,
            'face_tokens':face_tokens
        }
        response = requests.post(self.remove_url,data=data )
        if response.status_code ==200:
            results = response.json()
            return response.status_code,results
        return response,response.json()

    #人脸检索
    def Face_Search(self,image_path,outer_id):
        self.img_resize(image_path)
        files = {'image_file':open(image_path,'rb').read()}
        data = {
            'api_key':self.api_key,
            'api_secret':self.api_secret,
            'outer_id':outer_id,
        }
        response = requests.post(self.search_url,data=data,files=files)
        if response.status_code ==200:
            results = response.json()
            return response.status_code,results

        return response.status_code ,response.json()

if __name__ =='__main__':
    api_key = 'd7KyrJBh3NQeFfsUaQCaVMvkHeYykU0p'
    api_secret = 't4WbsJTPLo5XOquBlS2q8bNHJEJstzP3'
    create_url ='https://api-cn.faceplusplus.com/facepp/v3/faceset/create'  #创建人脸库url
    detect_url = 'https://api-cn.faceplusplus.com/facepp/v3/detect' #人脸检测url
    add_url = 'https://api-cn.faceplusplus.com/facepp/v3/faceset/addface' #添加人脸url
    search_url = 'https://api-cn.faceplusplus.com/facepp/v3/search'  #人脸检索url
    delete_url = 'https://api-cn.faceplusplus.com/facepp/v3/faceset/delete' #人脸库删除
    get_url = 'https://api-cn.faceplusplus.com/facepp/v3/faceset/getdetail' #获取人脸库信息
    get_fs_url = 'https://api-cn.faceplusplus.com/facepp/v3/faceset/getfacesets' #获取API Key下所有人脸库
    remove_url = ' https://api-cn.faceplusplus.com/facepp/v3/faceset/removeface'
    file_path =r'D:\baidu\image_1103'
    face_recognition = Face_Recognition(api_key,api_secret,create_url,detect_url,\
                                        add_url,search_url,delete_url,get_url,get_fs_url,remove_url)
    #创建人脸库
    # code,faceset_token = face_recognition.FaceSet_Create('白礁小学','12c311511fe94e63b067c0443781599e','12c311511fe94e63b067c0443781599e')
    # print(code,faceset_token) #234dcf9b96c55cda758760ed983c5cbb
    #删除人脸库
    # code,results = face_recognition.FaceSet_Delete('12c311511fe94e63b067c0443781599e')
    # print(code,results)
    #获取人脸库信息
    # code , results = face_recognition.FaceSet_Get('12c311511fe94e63b067c0443781599e')
    # print(code,results)
    #获取API Key下所有人脸库
    # code,results = face_recognition.FaceSet_GetFS()
    # print(code,results)
    #人脸检测
    # path =r'C:\Users\Admin\Desktop\1.jpg'
    # code,results = face_recognition.Face_Detect(path)
    # print(code,results)



    # 批量增加人脸
    # face_tokens =''
    # kv ={}
    # for i,pic in enumerate(os.listdir(file_path)):
    #     image_path = file_path + '\\' + pic
    #     code,face_token = face_recognition.Face_Detect(image_path)
    #     if code ==200 and face_token:
    #         code,results = face_recognition.Face_Add('12c311511fe94e63b067c0443781599e',face_token)
    #         if code ==200:
    #             kv[image_path] = face_token
    #         else:
    #             print('1:',image_path)
    #     else:
    #         print('2:',image_path,code,face_token)
    # print(kv)

    #人脸检索
    image_path =r'C:\Users\Admin\Desktop\1.jpg'
    code,result = face_recognition.Face_Search(image_path,'12c311511fe94e63b067c0443781599e')
    print(code,result)