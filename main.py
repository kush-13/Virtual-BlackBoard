import cv2
import numpy as np
from threading import Thread
from pynput import mouse
status = False


def on_click(x, y, button, pressed):
    global status
    if pressed:
        status = True
    else:
        status = False


def fun():
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()


Thread(target=fun).start()

print(cv2.__version__)

initBB = None  # bounding box for tracking object
board = np.ndarray(shape=(500, 500))

# camera = cv2.VideoCapture('036 epic-horses.mp4')
camera = cv2.VideoCapture(0)

OPENCV_OBJECT_TRACKERS = {
    "csrt": cv2.TrackerCSRT_create,
    "kcf": cv2.TrackerKCF_create,
    "boosting": cv2.TrackerBoosting_create,
    "mil": cv2.TrackerMIL_create,
    "tld": cv2.TrackerTLD_create,
    "medianflow": cv2.TrackerMedianFlow_create,
    "mosse": cv2.TrackerMOSSE_create
}

# choosing tracker of my own choice
tracker = OPENCV_OBJECT_TRACKERS['csrt']()

ret, image = camera.read()

while ret:
    frame = cv2.resize(image, (500, 500))
    # print(frame.shape)
    if initBB is not None:
        (success, box) = tracker.update(frame)
        if success:
            (x, y, w, h) = [int(v) for v in box]
            center = ((x+w//2), (y+h//2))
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), thickness=2)
            if status:
                cv2.circle(board, center, 10, (250, 0, 0), thickness=-1)
    cv2.imshow('video', frame)
    cv2.imshow('board', cv2.flip(board,1))
    key = cv2.waitKey(1)

    if key == ord("s"):
        initBB = cv2.selectROI("Frame", frame, fromCenter=False, showCrosshair=True)
        tracker.init(frame, initBB)

    if key == ord('e'):
        board = np.ndarray(shape=(500, 500))

    if key == 27:
        cv2.destroyAllWindows()
        camera.release()

    ret, image = camera.read()