import v2
import numpy as np


cam = cv2.VideoCapture(0)

def streaming():
    
    while True:
        ret, frame = cam.read()
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(frame, 1.3, 10)
        for (x,y,w,h) in faces:
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,0), 2)
            sub_face =frame[y:y+h, x:x+w]
           
        return cv2.imencode('.jpg', frame)[1].tobytes() 
