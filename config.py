# Grid dimensions (pixels)
GRID_W, GRID_H = 150, 1500

# Number of lanes in the BEV
LANE_COUNT = 4

# Size of each cell in grid (10 px tall)
CELL_SIZE = 10

# Canvas width in pixels (room for margins)
CANVAS_W = 300

# Vehicle icon size
CAR_W = GRID_W // LANE_COUNT
CAR_H = int(CAR_W * 2.5)

# Safety buffer around each car in cells
CAR_BUFFER = 6

# Offset BEV grid vertically upward to leave margin at bottom
VERTICAL_SHIFT = 250

# How often to re-run YOLO detection
UPDATE_EVERY_N_FRAMES = 4

# Classes to consider as vehicles from YOLO (car, bus, truck, etc.)
vehicle_classes = [2, 3, 5, 7]

# How much empty margin to leave on sides of BEV canvas
x_offset = (CANVAS_W - GRID_W) // 2
