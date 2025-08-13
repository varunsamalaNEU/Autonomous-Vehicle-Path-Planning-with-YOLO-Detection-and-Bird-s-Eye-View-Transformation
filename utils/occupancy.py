import numpy as np
import cv2
from config import *

# Build occupancy grid and draw detected cars in the BEV
def build_occupancy_grid(results, src, M, x_offset, canvas, car_icon_right, car_icon_left):
    grid_rows = GRID_H // CELL_SIZE
    occupancy = np.zeros((grid_rows, LANE_COUNT), dtype=np.uint8)

    for box in results.boxes:
        cls = int(box.cls[0])
        if cls not in vehicle_classes:
            continue

        # Grab YOLO box and find its bottom center (rear wheel region)
        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
        cx = (x1 + x2) / 2
        cy = y2

        # Only process if the point lies inside our road trapezoid
        if cv2.pointPolygonTest(src, (cx, cy), False) < 0:
            continue

        # Warp this point to BEV space
        warped = cv2.perspectiveTransform(np.array([[[cx, cy]]], dtype=np.float32), M)[0][0]
        gx = int(warped[0])

        # Stretch the y-coordinate to exaggerate spacing
        stretched_y = warped[1] * 1.1 # Try 1.3–2.0 for different stretch effects
        gy = int(stretched_y) - VERTICAL_SHIFT


        if gy < 0:
            continue

        # Determine grid cell (lane index and row index)
        lane_idx = int(gx / (GRID_W / LANE_COUNT))
        grid_y = gy // CELL_SIZE

        # Mark occupancy with a vertical buffer to account for car size
        if 0 <= grid_y < grid_rows and 0 <= lane_idx < LANE_COUNT:
            for dy in range(-CAR_BUFFER, CAR_BUFFER + 1):
                ny = grid_y + dy
                if 0 <= ny < grid_rows:
                    occupancy[ny, lane_idx] = 1

            # Draw the car icon (flipped depending on lane side)
            cx_px = int((lane_idx + 0.5) * (GRID_W // LANE_COUNT))
            cy_px = int(grid_y * CELL_SIZE)
            icon = car_icon_right if lane_idx in [2, 3] else car_icon_left
            icon_h, icon_w = icon.shape[:2]
            top_left_x = cx_px - icon_w // 2 + x_offset
            top_left_y = cy_px - icon_h // 2
            for c in range(3):
                alpha = icon[:, :, 3] / 255.0 if icon.shape[2] == 4 else 1.0
                canvas[top_left_y:top_left_y+icon_h, top_left_x:top_left_x+icon_w, c] = (
                    alpha * icon[:, :, c] + (1 - alpha) * canvas[top_left_y:top_left_y+icon_h, top_left_x:top_left_x+icon_w, c]
                )

    return occupancy
