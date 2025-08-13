import cv2
import numpy as np
import math
from config import *
from utils.perspective import get_perspective_transform
from utils.detection import load_model, run_detection
from utils.icons import load_all_icons
from utils.occupancy import build_occupancy_grid
from utils.drawing import draw_path, draw_flag_and_stop, draw_ego_vehicle
from astar import a_star
from utils.lane_lines import draw_lane_lines

# Load model and video
model = load_model()
cap = cv2.VideoCapture("asdf.mp4")

# Get frame dimensions
ret, frame = cap.read()
frame_h, frame_w = frame.shape[:2]
fps = cap.get(cv2.CAP_PROP_FPS)

# Setup transforms and icons
M, src = get_perspective_transform(frame_w, frame_h)
car_icon_right, car_icon_left, cam_car_icon, finish_icon, stop_icon = load_all_icons()

# Video writer - use canvas dimensions
out_w = frame_w + CANVAS_W
out_h = GRID_H  # Use original canvas height
out = cv2.VideoWriter("output.avi", cv2.VideoWriter_fourcc(*"XVID"), int(fps), (out_w, out_h))

cached_results = None
frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1
    annotated = frame.copy()

    # YOLO detection
    yolo_results, cached_results = run_detection(frame, frame_count, model, cached_results)

    # Draw bounding boxes
    for box in yolo_results.boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])
        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
        label = f"{model.names[cls_id]} {conf:.2f}"
        cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(annotated, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # BEV canvas - use original dimensions
    canvas = np.zeros((GRID_H, CANVAS_W, 3), dtype=np.uint8)
    canvas[:, :x_offset] = (30, 30, 30)
    canvas[:, -x_offset:] = (30, 30, 30)

    # Draw lanes and occupancy - back to original
    lane_spacing = GRID_W // LANE_COUNT
    draw_lane_lines(canvas, lane_spacing, x_offset)
    occupancy = build_occupancy_grid(cached_results, src, M, x_offset, canvas, car_icon_right, car_icon_left)
    
    # Path planning - use original grid dimensions
    grid_rows = GRID_H // CELL_SIZE
    start, goal = (grid_rows - 1, 2), (10, 2)
    path = a_star(occupancy, start, goal, allowed_lanes=[2, 3])
    
    # Path planning - back to original
    grid_rows = GRID_H // CELL_SIZE
    start, goal = (grid_rows - 1, 2), (10, 2)
    path = a_star(occupancy, start, goal, allowed_lanes=[2, 3])

    # Fallback path
    if not path or len(path) < 2:
        for dy in range(1, grid_rows):
            probe = (start[0] - dy, start[1])
            if 0 <= probe[0] < grid_rows and occupancy[probe[0], probe[1]] == 0:
                path = [start, probe]
            else:
                break

    # Draw path and vehicles
    draw_lane_lines(canvas, lane_spacing, x_offset)
    draw_path(canvas, path, x_offset, (0, 150, 0), frame_count)
    draw_flag_and_stop(canvas, path, goal, finish_icon, stop_icon, x_offset)
    draw_ego_vehicle(canvas, cam_car_icon, x_offset)

    # Combine frames - resize video to match canvas
    annotated_resized = cv2.resize(annotated, (frame_w, GRID_H))
    
    combined = np.zeros((GRID_H, out_w, 3), dtype=np.uint8)
    combined[:, :frame_w] = annotated_resized
    combined[:, frame_w:] = canvas

    # Display and save
    cv2.imshow("BEV + Path Planning", combined)
    out.write(combined)
    
    if cv2.waitKey(1) == 27:
        break

cap.release()
out.release()
cv2.destroyAllWindows()