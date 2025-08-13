import numpy as np
import cv2
from config import GRID_W, GRID_H

# Define the road trapezoid and warp it to a top-down rectangle
def get_perspective_transform(frame_w, frame_h):
    # Trapezoid points in the original frame (manually tweaked)
    src = np.float32([
        [-1250, 1280],
        [2500, 1280],
        [965, 725],
        [910, 725]

    # src = np.float32([
    #     [264, 136],
    #     [301, 136],
    #     [34, 174],
    #     [467, 168]

    ])

    # Scale those points based on actual frame size
    scale_x = frame_w / 2000
    scale_y = frame_h / 1100
    src[:, 0] *= scale_x
    src[:, 1] *= scale_y

    # Destination is a full rectangular grid from top-down view
    dst = np.float32([
        [0, GRID_H],
        [GRID_W, GRID_H],
        [GRID_W, 0],
        [0, 0]
    ])

    M = cv2.getPerspectiveTransform(src, dst)
    return M, src
