import cv2
from config import CAR_W, CAR_H

# Load and resize all necessary icons (cars, goal flag, stop sign)
def load_all_icons():
    right = cv2.imread("TOP_DOWN_CAR.png", cv2.IMREAD_UNCHANGED)
    left = cv2.imread("TOP_DOWN_CAR_REVERSED.png", cv2.IMREAD_UNCHANGED)
    cam = cv2.imread("CAM_CAR.png", cv2.IMREAD_UNCHANGED)
    finish = cv2.imread("Finish_flag.png", cv2.IMREAD_UNCHANGED)
    stop = cv2.imread("Stop_sign.png", cv2.IMREAD_UNCHANGED)
    
    # Resize car icons to fit lane width
    right = cv2.resize(right, (CAR_W, CAR_H))
    left = cv2.resize(left, (CAR_W, CAR_H))
    cam = cv2.resize(cam, (CAR_W, CAR_H))
    finish = cv2.resize(finish, (40, 40))
    stop = cv2.resize(stop, (40, 40))

    return right, left, cam, finish, stop
