import cv2

# Load a single frame from your video
video_path = "qwer.mp4"
cap = cv2.VideoCapture(video_path)
ret, frame = cap.read()
cap.release()

points = []

def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        print(f"Point: ({x}, {y})")
        cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)
        cv2.imshow("Frame", frame)

cv2.imshow("Frame", frame)
cv2.setMouseCallback("Frame", click_event)
cv2.waitKey(0)
cv2.destroyAllWindows()

print("Selected Points:", points)
