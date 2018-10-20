# -*- coding: utf-8 -*-
import numpy as np
import tensorflow as tf
from scipy import misc
import align_pospal.detect_face
import facenet_pospal as facenet
from common_util import rotate_cv2, z_rotate, get_max_face_area, get_crop_bounding_boxes, convert_distance_to_score, get_names_from_json, \
    get_encodings_from_json
import error_code
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

class Recognition:
    def __init__(self, model_checkpoint):
        self.debug = False
        self.detect = Detection()
        self.encoder = Encoder(model_checkpoint)

    def register_face(self, image, relative_code):
        err_code, face = self.detect.find_max_face(image)
        if err_code == error_code.ERROR_CODE_OK:
            return err_code, self.encoder.generate_embedding(face)
        return err_code, 'error'


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
