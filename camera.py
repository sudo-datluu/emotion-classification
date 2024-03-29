import cv2
import numpy as np 

from model import FacialExpressionModel

face_cas = cv2.CascadeClassifier('/model/haarcascade_frontalface_default.xml')
model = FacialExpressionModel("model/model.json", "model/model_weights.h5")
font = cv2.FONT_HERSHEY_SIMPLEX

class VideoStream(object):
	def __init__(self):
		self.video = cv2.VideoCapture(0)

	def __del__(self):
		self.video.release()

	def get_frame(self):
		_, fr = self.video.read()
		gray_fr = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
		faces = face_cas.detectMultiScale(gray_fr, 1.3, 5)

		for (x,y,w,h) in faces:
			fc = gray_fr[y:y+h, x:x+w]

			roi = cv2.resize(fc, (48,48))
			pred = model.predict_emotion(roi[np.newaxis, :, :, np.newaxis])

			cv2.putText(fr, pred, (x,y), font, 1, (255,255,0), 2)
			cv2.rectangle(fr, (x,y), (x+w, y+h), (255,0,0), 2)

		_, jpeg = cv2.imencode('.jpg', fr)
		return jpeg.tobytes()