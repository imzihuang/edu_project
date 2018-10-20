# -*- coding: utf-8 -*-
import os
import sys
from scipy import misc
import uuid
from datetime import datetime
from time import clock
from face_recognition_pospal import Recognition

class RecognitionService:
    def __init__(self, model_checkpoint):
        self.face_recognition = Recognition(model_checkpoint)

    def register_face(self, face_image, relative_code):
        return self.face_recognition.register_face(face_image, relative_code)