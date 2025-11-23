
#Facial Recognition code pipeline.
from deepface import DeepFace
import numpy as np
import matplotlib.pyplot as plt
import json
import cv2
import pandas as pd

#backends = ['opencv', 'ssd', 'dlib', 'mtcnn', 'deepface', 'retinaface']


def recognition(img_path, db_path, confidence_threshold):
    face_recognition = DeepFace.find(img_path=img_path, db_path=db_path, detector_backend='opencv')
    df = face_recognition[0]

    matched_images = []

    for idx, row in df.iloc[1:].iterrows():
        if(row['confidence'] >= confidence_threshold):
            matched_images.append(row['identity']) #identity means image path.
        else:
            print("No match found or model less confident!")
        
    return matched_images

    # for idx, row in df.iloc[1:].iterrows():
    #     img_path = row['identity']
    #     img = cv2.imread(img_path)
    #     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    #     if(row['confidence'] >= confidence_threshold):
    #         plt.imshow(img)
    #         plt.title(f"{img_path} || confidence: {row['confidence']}")
    #         plt.axis('off')
    #         plt.show()~
    #     else:
    #         print("No Match Found OR Model less confident!")



        