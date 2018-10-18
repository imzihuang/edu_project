# -*- coding: utf-8 -*-
import pickle
import os
import cv2
import numpy as np
import tensorflow as tf
from scipy import misc
import align_pospal.detect_face
import facenet_pospal as facenet
import json
import math
import uuid
from common_util import rotate_cv2, z_rotate, get_max_face_area, get_crop_bounding_boxes, convert_distance_to_score, get_names_from_json, \
    get_encodings_from_json
import error_code
from datetime import datetime
from mongoDB_helper import MongoDBHelper
from mysqlDB_helper import  mysqlDBHelper
from scipy.spatial import distance
from sklearn.metrics.pairwise import euclidean_distances
from time import  clock
#import pandas as pd
import json
class Face:
    def __init__(self):
        self.school_id = None
        self.class_id = None
        self.person_id = None
        self.face_id = None
        self.bounding_box = None
        self.image = None
        self.container_image = None
        self.feature = None

        self.group_id = None
        self.person_id = None
        self.face_url = None
        self.bounding_box = None
        self.image = None
        self.container_image = None
        self.embedding  = None

class Recognition:
    def __init__(self, model_checkpoint):
        self.debug = False
        self.detect = Detection()
        self.encoder = Encoder(model_checkpoint)
        self.identifier = Identifier()
        #self.db_helper = MongoDBHelper()
        self.db_helper = mysqlDBHelper()

    def register_identity(self, image, group_id, person_id, face_url):
        err_code, face = self.detect.find_max_face(image)
        if err_code == error_code.ERROR_CODE_OK:
            face.group_id = group_id
            face.person_id = person_id
            face.face_url = face_url
            face.embedding = self.encoder.generate_embedding(face)
            self.db_helper.insert_identity(face)

    def delete_identity(self, group_id, person_id):
        face = Face()
        face.group_id = group_id
        face.person_id = person_id
        return self.db_helper.delete_identity(face)

    def register_face(self, image, school_id, class_id,person_id, face_id):
        err_code, face = self.detect.find_max_face(image)
        if err_code == error_code.ERROR_CODE_OK:
            face.school_id = school_id
            face.class_id = class_id
            face.person_id = person_id
            face.face_id = face_id
            face.feature = self.encoder.generate_embedding(face)
            self.db_helper.insert_face(face)
            return err_code,face.feature
        return err_code,'error'

    def delete_face(self, school_id, class_id,person_id, face_id):
        face = Face()
        face.school_id = school_id
        face.class_id = class_id
        face.person_id = person_id
        face.face_id = face_id
        try:
            self.db_helper.delete_face(face)
            code = 0
        except:
            code = 1
        return code



    def identify(self,  df,image):
        bg = datetime.now()
        err_code, face = self.detect.find_max_face(image)
        if err_code == error_code.ERROR_CODE_OK:
            #group_faces = self.db_helper.find_face_embeddings(group_id)
            face.feature = self.encoder.generate_embedding(face)
            #person_id, score ,face_url= self.identifier.identify(face, group_faces)
            #return person_id, score, face_url
            dls= self.identifier.identify(face, df)
            return dls
        #return err_code, None, None,None
        return err_code

class Identifier:
    def __init__(self):
        # names_file = "face_data/names.json"
        # encodings_file = "face_data/encodings.json"
        # self.known_embs = get_encodings_from_json(encodings_file)
        # self.known_names = get_names_from_json(names_file)
        pass

    # 1
    def eudis1(self, v1, v2):
        return np.linalg.norm(v1 - v2)

    # 2
    def eudis2(self, v1, v2):
        return distance.euclidean(v1, v2)

    # 3
    def eudis3(self, v1, v2):
        return euclidean_distances(v1, v2)

    # 5
    def eudis5(self, v1, v2):
        dist = [(a - b) ** 2 for a, b in zip(v1, v2)]
        dist = math.sqrt(sum(dist))
        return dist


    def identify(self, face, group_faces):
        bg = datetime.now()
        dl = []
        if face.feature is not None:
            dis = group_faces['feature'].apply(self.eudis1, args=(face.feature,))
            group_faces['dis'] = dis
            group_faces=group_faces.sort_values(by='dis')[:1] #取前面5条数据
            for  result in zip(group_faces['face_id'],group_faces['person_id'],group_faces['dis'],group_faces['class_id']):
                kv = {}
                kv['confidence'] = round(convert_distance_to_score(result[2]) *100,2)
                kv['face_id'] = result[0]
                kv['person_id'] = result[1]
                kv['class_id'] = result[3]
                kv['tag'] ='new tag'
                dl.append(kv)
            return  dl

class Encoder:
    def __init__(self, model_checkpoint):
        self.sess = tf.Session()
        with self.sess.as_default():
            facenet.load_model(model_checkpoint)

    def generate_embedding(self, face):
        # Get input and output tensors
        images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
        embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
        phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")

        prewhiten_face = facenet.prewhiten(face.image)
        # Run forward pass to calculate embeddings
        feed_dict = {images_placeholder: [prewhiten_face], phase_train_placeholder: False}
        return self.sess.run(embeddings, feed_dict=feed_dict)[0]


class Detection:
    # face detection parameters
    minsize = 20  # minimum size of face
    threshold = [0.6, 0.7, 0.7]  # three steps's threshold
    factor = 0.709  # scale factor
    gpu_memory_fraction = 0.3

    def __init__(self, face_crop_size=160, face_crop_margin=32):
        self.pnet, self.rnet, self.onet = self._setup_mtcnn()
        self.face_crop_size = face_crop_size
        self.face_crop_margin = face_crop_margin

    def _setup_mtcnn(self):
        with tf.Graph().as_default():
            gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=self.gpu_memory_fraction)
            sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
            with sess.as_default():
                return align_pospal.detect_face.create_mtcnn(sess, None)

    def find_max_face(self, image, integral_limit=0.095):
        bounding_boxes, points = align_pospal.detect_face.detect_face(image, self.minsize,
                                                               self.pnet, self.rnet, self.onet,
                                                               self.threshold, self.factor)
        if len(bounding_boxes) >= 1:
            max_area, index = get_max_face_area(bounding_boxes, image)
            bb = bounding_boxes[index]
            img_size = np.asarray(image.shape)[0:2]
            aa = np.zeros(4, dtype=np.int32)
            aa[0] = np.maximum(bb[0], 0)
            aa[1] = np.maximum(bb[1], 0)
            aa[2] = np.minimum(bb[2], img_size[1])
            aa[3] = np.minimum(bb[3], img_size[0])
            area_big = (int(bb[2]) - int(bb[0])) * (int(bb[3]) - int(bb[1]))
            area_small = (aa[2] - aa[0]) * (aa[3] - aa[1])
            integral = area_small / area_big
            if integral <= integral_limit:
                print("face integral is %s" % integral)
                return error_code.ERROR_CODE_INTEGRAL_LOW, None
            else:
                face = Face()
                face.container_image = image
                face.bounding_box = np.zeros(4, dtype=np.int32)
                crop_bb = get_crop_bounding_boxes(bb, img_size)
                face.bounding_box[0], face.bounding_box[1], face.bounding_box[2], face.bounding_box[3] = crop_bb
                cropped = image[crop_bb[1]:crop_bb[3], crop_bb[0]:crop_bb[2], :]
                point_left_eye = (points[0][index], points[5][index])
                point_right_eye = (points[1][index], points[6][index])
                image_rotate = rotate_cv2(cropped, z_rotate(point_left_eye, point_right_eye),
                                          (crop_bb[3] - crop_bb[1], crop_bb[2] - crop_bb[0]))
                face.image = misc.imresize(image_rotate, (self.face_crop_size, self.face_crop_size), interp='bilinear')
                # misc.imsave("D:\\aaa\\" + str(uuid.uuid1()) + '.jpg', face.image)

                return error_code.ERROR_CODE_OK, face
        else:
            return error_code.ERROR_CODE_NO_FACE, None
