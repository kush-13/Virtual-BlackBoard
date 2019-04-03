import cv2
import numpy as np
import numpy as np
import imutils

camera = cv2.VideoCapture('http://192.168.0.13:8080/video')
# cv2.imshow('wewe',camera.read()[1])
lower_blue = np.array([110-10, 50, 50])
upper_blue = np.array([130, 255, 255])

#  95, 27, 42 lower range
#  121, 45, 43 upper range
def exploit(img):
    result= img.copy()
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255), (255, 255, 255)]
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img = cv2.inRange(img, lower_blue, upper_blue)  # masking
    cnt = cv2.findContours(original, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[1]
    box=cv2.boxPoints(cv2.minAreaRect(cnt[0]))
    cv2.drawContours(img, [box], -1, (255, 0, 0), 2)
    # kernel = cv2.getStructuringElement(cv2.MORPH_ERODE, (3, 3))
    # img = cv2.erode(img, kernel, iterations=1)
    # img = imutils.auto_canny(img)
    # img = cv2.Canny(img, 10, 50)
    # img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    # img = cv2.dilate(img, kernel, iterations=1)

    # if len(cnt) != 0:
    #     for c in cnt:
    #         # area = cv2.contourArea(c)
    #         box = cv2.minAreaRect(c)
    #         box = cv2.boxPoints(box)
    #         centre = (box[0, 0:].sum()/2, box[1, 0:].sum()/2)
    #         print(centre)
    #         print(type(box))
    #         print(box)
    #         cv2.circle(result, centre, 10, (255, 0, 0))
            # print(box)
    return img
    # cv2.imshow('img', img)


while 1:
    try:
        image = camera.read()[1]
        cv2.imshow('image', exploit(image))
        cv2.waitKey(1)
    except:
        cv2.destroyAllWindows()
        camera.release()
        break
