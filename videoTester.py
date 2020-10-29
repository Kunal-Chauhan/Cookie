import os
import cv2
import numpy as np
import faces

face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read('trainingData.yml')

name = {0: "unknown", 1: "khushi"}


def live():
    cap = cv2.VideoCapture(0)
    i = 0
    a = 0
    while a < 30:
        a = a+1
        ret, test_img = cap.read()
        faces_detected, gray_img = faces.faceDetection(test_img)
        cv2.waitKey(10)
        resized_img = cv2.resize(test_img, (550, 550))
        for face in faces_detected:
            (x, y, w, h) = face
            roi_gray = gray_img[y:y+h, x:x+w]
            label, confidence = face_recognizer.predict(roi_gray)
            predicted_name = name[label]
            a = a+1
            if confidence < 70:
                i = i+1
        if cv2.waitKey(10) == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    if i >= 3:
        return 1
    else:
        return 0


def check():
    print("cv2")
