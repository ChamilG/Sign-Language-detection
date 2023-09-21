import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import tensorflow as tf
import cv2
import mediapipe as mp
from keras.models import load_model
import numpy as np
import time
import pandas as pd


model = load_model('Model/smnist.h5')

mphands = mp.solutions.hands
hands = mphands.Hands()
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
_, frame = cap.read()
h, w, c = frame.shape

analysisframe = ''
letterpred = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y']

while True:
    _, frame = cap.read()
    
    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    # SPACE pressed
    # SPACE pressed
    analysisframe = frame
    showframe = analysisframe
    cv2.imshow("Frame", showframe)
    framergbanalysis = cv2.cvtColor(analysisframe, cv2.COLOR_BGR2RGB)
    resultanalysis = hands.process(framergbanalysis)
    hand_landmarksanalysis = resultanalysis.multi_hand_landmarks
    if hand_landmarksanalysis:
        print('Success')
        for handLMsanalysis in hand_landmarksanalysis:
            x_max = 0
            y_max = 0
            x_min = w
            y_min = h
            # creating the bounding box
            for lmanalysis in handLMsanalysis.landmark:
                x, y = int(lmanalysis.x * w), int(lmanalysis.y * h)  # this is to scale back the coordinates into pixel form(initially it is been normalized in range(0,1))
                if x > x_max:
                    x_max = x
                if x < x_min:
                    x_min = x
                if y > y_max:
                    y_max = y
                if y < y_min:
                    y_min = y
            y_min -= 20
            y_max += 20
            x_min -= 20
            x_max += 20 

            analysisframe = cv2.cvtColor(analysisframe, cv2.COLOR_BGR2GRAY)
            analysisframe = analysisframe[y_min:y_max, x_min:x_max]
            analysisframe = cv2.resize(analysisframe,(28,28))


            nlist = []
            rows,cols = analysisframe.shape
            for i in range(rows):
                for j in range(cols):
                    k = analysisframe[i,j]
                    nlist.append(k)
            
            datan = pd.DataFrame(nlist).T
            colname = []
            for val in range(784):
                colname.append(val)
            datan.columns = colname

            pixeldata = datan.values
            pixeldata = pixeldata / 255
            pixeldata = pixeldata.reshape(-1,28,28,1)
                # cv2.imshow("Frame", frame)

            prediction = model.predict(pixeldata)
            predarray = np.array(prediction[0])
            letter_prediction_dict = {letterpred[i]: predarray[i] for i in range(len(letterpred))}
            predarrayordered = sorted(predarray, reverse=True)
            high1 = predarrayordered[0]
            high2 = predarrayordered[1]
            high3 = predarrayordered[2]
            for key,value in letter_prediction_dict.items():
                if value==high1:
                    print("Predicted Character 1: ", key)
                    print('Confidence 1: ', 100*value)
                elif value==high2:
                    print("Predicted Character 2: ", key)
                    print('Confidence 2: ', 100*value)
                elif value==high3:
                    print("Predicted Character 3: ", key)
                    print('Confidence 3: ', 100*value)
            time.sleep(5)

# cap.release()
# cv2.destroyAllWindows()