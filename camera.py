import cv2
import numpy as np
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import datetime
import time
import uuid
import csv
import json
from firebase import firebase
from google.cloud import storage 
import firebase_admin
from firebase_admin import credentials, firestore, storage
#from apscheduler.schedulers.background import BackgroundScheduler

#scheduler = BackgroundScheduler()
#scheduler.start()



cam = cv2.VideoCapture("rtsp://192.168.1.1:554/live/ch00_1")
face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cred = credentials.Certificate('C:\\Users\\PROTOSEM\\Downloads\\google.json')
firebase = firebase.FirebaseApplication('https://kittycam-nivetha.firebaseio.com/')



def streaming():
    
    while True:
        ret, frame = cam.read()
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(frame, 1.3, 10)
        for (x,y,w,h) in faces:
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,0), 2)
            sub_face =frame[y:y+h, x:x+w]
        cv2.imshow("frame",frame)
        if cv2.waitKey(1) & 0xFF==ord('q'):
            break    

            
        #return cv2.imencode('.jpg', frame)[1].tobytes() 


    
def detection():
    length = 5
    count = 1
    i=1
    id=uuid.uuid1()
    user="unknown"
    ts = time.time()
    date_d = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    time_Stamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    while True:
        ret, frame = cam.read()
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 10)
        for (x,y,w,h) in faces:
            cv2.rectangle(gray, (x,y), (x+w,y+h), (0,0,0), 2)
            sub_face =gray[y:y+h, x:x+w]
            while(count<=20):
                FaceFileName = "datasets/"+ str(count) + ".jpg"
                cv2.imwrite(FaceFileName,sub_face)
                cv2,imshow("frame",frame)
                f1 = cv2.imread("datasets/"+str(count)+".jpg")
                f2 = str(f1)
                f3 = np.array(f2)
                f4 = f3.tolist()
                count = count+1
                for i in range(length):
                    send_mail("datasets/"+str(count)+".jpg")
                    print("mail sent")
                    send_data(user,count,FaceFileName,sub_face,date_d,time_Stamp,f4)
                    print("data sent to firebase")
                    send_csv(length,user,count,date_d,time_Stamp,id)
                    print("data sent to csv")


def send_mail(ImgFileName):
    img_data = open(ImgFileName, 'rb').read()
    msg = MIMEMultipart()
    msg['Subject'] = 'Notification'
    print("Image loaded")
    user = "nivetha.19.1@protosem.tech"
    password= "AllisWell17" 
    user1 = "madhinive@gmail.com"

    text = MIMEText("There is an Alert....!!!")
    msg.attach(text)
    image = MIMEImage(img_data, name=os.path.basename(ImgFileName))
    msg.attach(image)

    s = smtplib.SMTP('smtp.gmail.com:587')
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(user,password)
    s.sendmail(user,user1, msg.as_string())
    s.quit()

def send_data(user,count,FaceFileName,sub_face,date_d,time_Stamp,f4):
    result1=firebase.post('/data',{'No':count,"name":user,"Imagepath":FaceFileName,"date":date_d,"time":time_Stamp,"image":f4})
    print("data saved",result1)

def send_csv(length,user,count,date_d,time_Stamp,id):
    while(length>0):
        with open('datassS.csv', 'w') as myFile:
            writer = csv.writer(myFile)
            writer.writerow(['S_no','Name','Image','Image path','date','Time','uuid'])
            num=0
            for x in range(0,length):
                num=num+1
                facedata=[num,str(user),str(count)+".jpg","datasets/."+str(count)+".jpg",date_d,time_Stamp,id]
                writer = csv.writer(myFile)
                writer.writerow(facedata)
            myFile.close()



streaming()





    