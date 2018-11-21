# coding=utf-8
import numpy as np
import json
import math
import cv2
import uuid
from random import randint


def rotate_cv2(image, angle, img_size):
    height, width = img_size
    center = (width / 2, height / 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated_img = cv2.warpAffine(image, M, (width, height))
    return rotated_img

def z_rotate(point_left_eye, point_right_eye):
    x1, y1 = point_left_eye
    x2, y2 = point_right_eye
    if y2 - y1 == 0:
        return 0
    if x2 - x1 == 0:
        return 90 if y2 - y1 > 0 else -90

    tan_x = (y2 - y1) / (x2 - x1)
    return math.atan(tan_x) * 180 / math.pi


def get_max_face_area(bounding_boxes, image):
    max_face_area = 0
    index = 0
    for i, bb in enumerate(bounding_boxes):
        img_size = np.asarray(image.shape)[0:2]
        aa = np.zeros(4, dtype=np.int32)
        aa[0] = np.maximum(bb[0], 0)
        aa[1] = np.maximum(bb[1], 0)
        aa[2] = np.minimum(bb[2], img_size[1])
        aa[3] = np.minimum(bb[3], img_size[0])
        area = (aa[2] - aa[0]) * (aa[3] - aa[1])
        if area > max_face_area:
            max_face_area = area
            index = i
    return max_face_area, index


def get_crop_bounding_boxes(bounding_boxes, image_size, extend_proportion=0.0):
    # bounding_boxed: left, top, right, bottom
    left, top, right, bottom = bounding_boxes[0:4]
    left, top, right, bottom = int(left), int(top), int(right), int(bottom)
    image_height, image_width = image_size

    bb_height = bottom - top
    bb_width = right - left
    bb_max_edge = max(bb_height, bb_width)
    extend_size = bb_max_edge * extend_proportion
    # expected_size = (bb_max_edge + extend_size * 2)
    expected_size = int(bb_max_edge + extend_size * 2)
    if left + (image_width - right) < expected_size - bb_width:
        # 宽度不够拓展, 缩短size
        expected_size -= ((expected_size - bb_width) - (left + image_width - right))
    if top + (image_height - bottom) < expected_size - bb_height:
        # 高度不够拓展，缩短size
        expected_size -= ((expected_size - bb_height) - (top + image_height - bottom))

    # margin = (left, top, right, bottom)
    margin_horizon = expected_size - bb_width
    margin_vertical = expected_size - bb_height
    expected_left = 0
    expected_right = 0
    expected_top = 0
    expected_bottom = 0
    margin_left = int(margin_horizon / 2)
    margin_right = margin_horizon - margin_left
    margin_top = int(margin_vertical / 2)
    margin_bottom = margin_vertical - margin_top
    if margin_left <= left and margin_right <= image_width - right:
        expected_left = left - margin_left
        expected_right = right + margin_right
    elif margin_left <= left and margin_right > image_width - right:
        expected_right = image_width
        expected_left = left - (margin_horizon - (image_width - right))
    elif margin_left > left and margin_right <= image_width - right:
        expected_left = 0
        expected_right = right + (margin_horizon - left)

    if margin_top <= top and margin_bottom <= image_height - bottom:
        expected_top = top - margin_top
        expected_bottom = bottom + margin_bottom
    elif margin_top <= top and margin_bottom > image_height - bottom:
        expected_bottom = image_height
        expected_top = top - (margin_vertical - (image_height - bottom))
    elif margin_top > top and margin_bottom <= image_height - bottom:
        expected_top = 0
        expected_bottom = bottom + (margin_vertical - top)

    return [int(expected_left), int(expected_top), int(expected_right), int(expected_bottom)]


def convert_distance_to_score(x, min_threshold=0.6, max_threshold=1.0):
    # min_threshold 小于最小阈值，认为100%是这个人
    # max_threshold 等于最大阈值，认为50%是这个人，即可能为真，可能为假
    a = -0.5 / (max_threshold - min_threshold)
    b = (max_threshold - 0.5 * min_threshold) / (max_threshold - min_threshold)
    # return 1 - 0.5 / threshold * x
    return min(a * x + b, 1)


def get_names_from_json(names_json_file):
    with open(names_json_file, "r") as f:
        names = json.load(f)
    return names


def get_encodings_from_json(encodings_json_file):
    with open(encodings_json_file, "r") as f:
        encodings = json.load(f)

    known_encodings = []
    for encoding in encodings:
        known_encodings.append(np.array(encoding))
    return np.array(known_encodings)


def create_id():
    return uuid.uuid4().get_hex()

def create_verifycode():
    """
    生成注册验证码
    :return:
    """
    verify_code = ''.join((str(randint(0, 9)) for _ in range(6)))
    return verify_code