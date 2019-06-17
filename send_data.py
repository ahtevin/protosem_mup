from firebase import firebase
from google.cloud import storage 
import firebase_admin
import base64
import cv2
import json 
from firebase_admin import credentials, firestore, storage
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from camera import cam



cred = credentials.Certificate('C:\\Users\\PROTOSEM\\Downloads\\google.json')
firebase = firebase.FirebaseApplication('https://kiitycam.firebaseio.com/')
print(result1)