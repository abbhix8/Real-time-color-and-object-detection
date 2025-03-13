import cv2
import numpy as np
from ultralytics import YOLO

# Load the YOLOv8 model (pre-trained on the COCO dataset)
model = YOLO('yolov8n.pt')  # Use 'yolov8n.pt' for a faster, smaller model

# Function to find the object closest to the clicked point
def get_closest_object(x, y, detections):
    min_distance = float("inf")
    closest_object = None
    for det in detections:
        # Extract bounding box coordinates and class ID
        x1, y1, x2, y2, conf, class_id = det
        center_x, center_y = (x1 + x2) / 2, (y1 + y2) / 2
        distance = np.sqrt((center_x - x)**2 + (center_y - y)**2)
        if distance < min_distance:
            min_distance = distance
            closest_object = (x1, y1, x2, y2, class_id)
    return closest_object

# Callback function for mouse events
def mouse_click(event, x, y, flags, param):
    global clicked, click_x, click_y
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked = True
        click_x, click_y = x, y

# Initialize variables
clicked = False
click_x = click_y = 0

# Open webcam
cap = cv2.VideoCapture(0)
cv2.namedWindow("Webcam Feed")
cv2.setMouseCallback("Webcam Feed", mouse_click)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame. Exiting.")
        break

    # Run YOLOv8 detection with a lower confidence threshold
    results = model.predict(frame, conf=0.3)  # Lowered confidence threshold to 0.3
    detections = []
    for result in results[0].boxes.data.tolist():
        x1, y1, x2, y2, conf, class_id = result
        detections.append([x1, y1, x2, y2, conf, int(class_id)])

    # Draw bounding boxes and labels for all detected objects
    for det in detections:
        x1, y1, x2, y2, conf, class_id = map(int, det)
        label = model.names[class_id]
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Highlight the object closest to the clicked point
    if clicked:
        clicked = False  # Reset clicked state
        closest_object = get_closest_object(click_x, click_y, detections)
        if closest_object:
            x1, y1, x2, y2, class_id = map(int, closest_object)
            label = model.names[class_id]
            # Draw a red bounding box for the selected object
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(frame, f"Selected: {label}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # Show the live video feed
    cv2.imshow("Webcam Feed", frame)

    # Quit with 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
