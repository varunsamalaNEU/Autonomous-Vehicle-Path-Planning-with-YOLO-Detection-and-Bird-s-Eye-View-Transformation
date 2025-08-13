import cv2
from config import GRID_H, LANE_COUNT

# Draw vertical lane dividers on the BEV canvas
def draw_lane_lines(canvas, lane_spacing, x_offset):
    overlay = canvas.copy()

    for i in range(1, LANE_COUNT):
        x = int(i * lane_spacing + x_offset)
        color = (0, 255, 255) if i == 2 else (255, 255, 255)  # highlight center line
        cv2.line(overlay, (x, 0), (x, GRID_H), color, 2)

    # Blend overlay lightly so lane lines aren’t too harsh
    alpha = 0.2
    canvas[:] = cv2.addWeighted(overlay, alpha, canvas, 1 - alpha, 0)
