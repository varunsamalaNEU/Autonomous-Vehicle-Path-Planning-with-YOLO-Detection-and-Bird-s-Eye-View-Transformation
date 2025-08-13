import cv2
import numpy as np
from config import *

# Draws a thick green path line based on the planned A* path
def draw_path(canvas, path, x_offset, base_color=(0, 150, 0), frame_count=0):
    lane_spacing = GRID_W // LANE_COUNT

    # 1. Draw the solid base path (static dark green line)
    for i in range(1, len(path)):
        gy1, gx1 = path[i - 1]
        gy2, gx2 = path[i]
        px1 = int((gx1 + 0.5) * lane_spacing + x_offset)
        py1 = int((gy1 + 0.5) * CELL_SIZE)
        px2 = int((gx2 + 0.5) * lane_spacing + x_offset)
        py2 = int((gy2 + 0.5) * CELL_SIZE)
        cv2.line(canvas, (px1, py1), (px2, py2), base_color, 15)

    # 2. Pulse effect: animates the path to show direction
    segment_spacing = 30
    pulse_length = 9
    total_cycle = segment_spacing + pulse_length
    speed_factor = 1
    pulse_offset = (total_cycle - (frame_count * speed_factor) % total_cycle) % total_cycle


    for i in range(1, len(path)):
        if (i + pulse_offset) % total_cycle < pulse_length:
            gy1, gx1 = path[i - 1]
            gy2, gx2 = path[i]
            px1 = int((gx1 + 0.5) * lane_spacing + x_offset)
            py1 = int((gy1 + 0.5) * CELL_SIZE)
            px2 = int((gx2 + 0.5) * lane_spacing + x_offset)
            py2 = int((gy2 + 0.5) * CELL_SIZE)
            cv2.line(canvas, (px1, py1), (px2, py2), (0, 255, 0), 15)  

# Places the finish flag icon at the goal, and stop sign if we can't reach it
def draw_flag_and_stop(canvas, path, goal, finish_icon, stop_icon, x_offset):
    goal_y, goal_x = goal
    flag_h, flag_w = finish_icon.shape[:2]
    flag_cx = int((goal_x + 0.5) * (GRID_W // LANE_COUNT) + x_offset)
    flag_cy = int((goal_y + 0.5) * CELL_SIZE)
    flag_x = flag_cx - flag_w // 2
    flag_y = flag_cy - flag_h // 2

    # Paste the flag icon using alpha blending if transparent
    if finish_icon.shape[2] == 4:
        alpha = finish_icon[:, :, 3] / 255.0
        for c in range(3):
            canvas[flag_y:flag_y+flag_h, flag_x:flag_x+flag_w, c] = (
                alpha * finish_icon[:, :, c] +
                (1 - alpha) * canvas[flag_y:flag_y+flag_h, flag_x:flag_x+flag_w, c]
            )
    else:
        canvas[flag_y:flag_y+flag_h, flag_x:flag_x+flag_w] = finish_icon
    # If the goal wasn't reached properly, add stop sign at last reachable point
    if not path or path[-1][0] > goal_y + 2:
        last_gy, last_gx = path[-1]
        stop_h, stop_w = stop_icon.shape[:2]
        stop_cx = int((last_gx + 0.5) * (GRID_W // LANE_COUNT) + x_offset)
        stop_cy = int((last_gy + 0.5) * CELL_SIZE)
        stop_x = stop_cx - stop_w // 2
        stop_y = stop_cy - stop_h // 2

        if stop_icon.shape[2] == 4:
            alpha = stop_icon[:, :, 3] / 255.0
            for c in range(3):
                canvas[stop_y:stop_y+stop_h, stop_x:stop_x+stop_w, c] = (
                    alpha * stop_icon[:, :, c] +
                    (1 - alpha) * canvas[stop_y:stop_y+stop_h, stop_x:stop_x+stop_w, c]
                )
        else:
            canvas[stop_y:stop_y+stop_h, stop_x:stop_x+stop_w] = stop_icon
            
# Draw ego vehicle icon at the bottom of the canvas (centered in lane 2)
def draw_ego_vehicle(canvas, cam_car_icon, x_offset):
    lane_spacing = GRID_W // LANE_COUNT
    ego_lane_idx = 2
    ego_grid_y = GRID_H // CELL_SIZE - 1
    ego_cx_px = int((ego_lane_idx + 0.5) * lane_spacing + x_offset)
    ego_cy_px = int(ego_grid_y * CELL_SIZE)

    icon_h, icon_w = cam_car_icon.shape[:2]
    top_left_x = ego_cx_px - icon_w // 2
    top_left_y = ego_cy_px - icon_h // 2
    top_left_y = max(0, min(canvas.shape[0] - icon_h, top_left_y))

    if cam_car_icon.shape[2] == 4:
        alpha = cam_car_icon[:, :, 3] / 255.0
        for c in range(3):
            canvas[top_left_y:top_left_y+icon_h, top_left_x:top_left_x+icon_w, c] = (
                alpha * cam_car_icon[:, :, c] +
                (1 - alpha) * canvas[top_left_y:top_left_y+icon_h, top_left_x:top_left_x+icon_w, c]
            )
    else:
        canvas[top_left_y:top_left_y+icon_h, top_left_x:top_left_x+icon_w] = cam_car_icon
