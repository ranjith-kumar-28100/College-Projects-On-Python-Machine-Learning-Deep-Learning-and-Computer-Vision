import cv2 #package for computer vision
import serial
import time
import datetime
"""package for sending automated mails for the security issues"""
from flask import Flask 
from flask_mail import Mail, Message
import os
#connecting with the arduino board using serial package
try:
        ser = serial.Serial("COM6", 9600, timeout=1)
        time.sleep(2)
        print(ser)
except Exception as e:
        print(e)

#creating  and traing the face classifier with preexisting hascade classifier file
upperbody_classifier= cv2.CascadeClassifier('haarcascade_upperbody.xml')
face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#sending the automated mail using Flask and Flask-mail
def alert():
        
        app = Flask(__name__)
        mail_settings = {
            "MAIL_SERVER": 'smtp.gmail.com',
            "MAIL_PORT": 465,
            "MAIL_USE_TLS": False,
            "MAIL_USE_SSL": True,
            "MAIL_USERNAME": 'email',
            "MAIL_PASSWORD": 'password'
                }
        app.config.update(mail_settings)
        mail =  Mail(app)
        if __name__ == '__main__':
                with app.app_context():
                        msg = Message(subject = "Security Breach", sender = app.config.get("MAIL_USERNAME"),recipients=["anurag9799@gmail.com"],body = "some one has entered the room!")
                        mail.send(msg)

#code for human detection 
def human_detector(frame, size=0.5):
    
    img = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces= face_classifier.detectMultiScale(img,1.3,5)
    now = datetime.datetime.now()
    hr = now.hour

    
    body = upperbody_classifier.detectMultiScale(img,1.3,5)
    if faces is () and body is():
        print('no human found')
        command = str.encode('0')
        ser.write(command) #sending the value 0 to the arduino board
    else:
        for x,y,w,h in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,20,147),2)
            cv2.imshow('img',img)
            cv2.waitKey(0)

            if hr>12:
                    alert()

            command = str.encode('1')
            ser.write(command) #sending the value 1 to the arduino board
            time.sleep(2)

capture = cv2.VideoCapture(0) #switching on the web camera


while(True):
    ret, frame = capture.read()
    human_detector(frame)

