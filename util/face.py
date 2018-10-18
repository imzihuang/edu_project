# -*- coding: utf-8 -*-
import os
import sys
from scipy import misc
import uuid
from datetime import datetime
from time import clock
import pandas as pd
from face_recognition_pospal import Recognition

class RecognitionService:
    def __init__(self, model_checkpoint):
        self.face_recognition = Recognition(model_checkpoint)

    def register_identity(self, face_image, group_id, person_id, face_url):
        return self.face_recognition.register_identity(face_image, group_id, person_id, face_url)

    def delete_identity(self, group_id, person_id):
        return self.face_recognition.delete_identity(group_id, person_id)

    def register_face(self, face_image,school_id, class_id,person_id, face_id):
        return self.face_recognition.register_face(face_image,school_id, class_id,person_id, face_id)

    def delete_face(self, school_id, class_id,person_id, face_id):
        return self.face_recognition.delete_face(school_id, class_id,person_id, face_id)

    def recognition_face(self, df, face_image):
        dls = self.face_recognition.identify( df,face_image)
        return dls