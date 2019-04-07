import cv2
import numpy as np


camera = cv2.VideoCapture('https://192.168.0.10:8080/video')
lower_blue = np.array([110-10, 50, 50])
upper_blue = np.array([130, 255, 255])
(h,w,c)=camera.read()[1].shape
board=np.zeros((h,w,c),dtype='uint8')
while 1:                 
    img = camera.read()[1]
    orig = img.copy()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(img, lower_blue, upper_blue)
    edged = cv2.Canny(mask, 50, 100)
    cnt = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]
    if len(cnt)>0:
	    areas = [cv2.contourArea(c) for c in cnt]
	    max_index = np.argmax(areas)
	    if cv2.contourArea(cnt[max_index])>500:
	        rect = cv2.minAreaRect(cnt[max_index])
	        box = cv2.boxPoints(rect)
	        box = np.int0(box)
	        centre = (box[:,0].sum()//4,box[:,1].sum()//4)
	        cv2.drawContours(orig,[box], -1, (0,0,255),6)
	        cv2.circle(board, centre,9,(0,255,0),-1)
	        orig = orig+board*100
    cv2.imshow('ass', orig)
    cv2.imshow('final', board)
    k=cv2.waitKey(1)
    if k == 27:
        camera.release()
        break
    elif k==ord('1'):
        board=np.zeros((h,w,c),dtype='uint8')

