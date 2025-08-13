from ultralytics import YOLO
from config import UPDATE_EVERY_N_FRAMES

# Load YOLOv8n model
def load_model():
    return YOLO("yolov8n.pt")

# Run YOLO detection, and only update cached results every N frames
def run_detection(frame, frame_count, model, cached_results):
    results = model(frame, verbose=False, conf=0.15)[0]
    if frame_count % UPDATE_EVERY_N_FRAMES == 0 or cached_results is None:
        cached_results = results
    return results, cached_results


