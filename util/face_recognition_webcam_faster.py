# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 15:22:45 2018

@author: Mloong
"""

import face_recognition
import cv2
import uuid
from face_recognition_api import Face_Recognition_YYL


api_key = 'd7KyrJBh3NQeFfsUaQCaVMvkHeYykU0p'
api_secret = 't4WbsJTPLo5XOquBlS2q8bNHJEJstzP3'
search_url = 'https://api-cn.faceplusplus.com/facepp/v3/search'  # 人脸检索url
face_recognition_yyl = Face_Recognition_YYL(api_key, api_secret, '', '', '', '',search_url, '', '', ''  )


#video_capture = cv2.VideoCapture(0)
#打开网络摄像头2台，192.168.62.61 和 192.168.62.62
#video_capture = cv2.VideoCapture("rtsp://admin:jw123456@192.168.62.61:554/mpeg4/ch1/main/av_stream")
video_capture = cv2.VideoCapture("rtsp://admin:jw123456@192.168.62.62:554/mpeg4/ch1/main/av_stream")

process_this_frame = True
school_id = ''
while True:
    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_samll_frame = small_frame[:, :, ::-1] #bgr转rgb

    if process_this_frame:
        face_locations = face_recognition.face_locations(rgb_samll_frame)
        if face_locations:
            image_path = '../static/upload/' + str(uuid.uuid1()) + '.jpg'
            cv2.imwrite(image_path,frame)
            code ,results = face_recognition_yyl.Face_Search(image_path,school_id)

            

        # face_encodings = face_recognition.face_encodings(rgb_samll_frame, face_locations)
        # face_names = []
        # for face_encoding in face_encodings:
        #     matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        #     name = 'unkown'
        #     if True in matches:
        #         first_match_index = matches.index(True)
        #         name = known_face_names[first_match_index]
        #     face_names.append(name)
    process_this_frame = not process_this_frame
    #
    # cv2.imshow('Video', frame)
    #
    # for (top, right, bottom, left), name in zip(face_locations, face_names):
    #     top *= 1
    #     right *= 1
    #     bottom *= 1
    #     left *= 1
    #     # Draw a box around the face
    #     cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
    #
    #     # Draw a label with a name below the face
    #     cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
    #     font = cv2.FONT_HERSHEY_DUPLEX
    #     cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
    #
    #     # Display the resulting image
    # cv2.imshow('Video', frame)
    #
    # # Hit 'q' on the keyboard to quit!
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
