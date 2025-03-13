import cv2
import numpy as np

# Define color names with RGB values
color_names = {
    "Red": (255, 0, 0),
    "Green": (0, 255, 0),
    "Blue": (0, 0, 255),
    "Yellow": (255, 255, 0),
    "Cyan": (0, 255, 255),
    "Magenta": (255, 0, 255),
    "Black": (0, 0, 0),
    "White": (255, 255, 255),
    "Gray": (128, 128, 128)
}

# Function to get the closest color name
def get_color_name(r, g, b):
    min_distance = float("inf")
    closest_color = "Unknown"
    for name, (cr, cg, cb) in color_names.items():
        distance = np.sqrt((r - cr)**2 + (g - cg)**2 + (b - cb)**2)
        if distance < min_distance:
            min_distance = distance
            closest_color = name
    return closest_color

# Callback function for mouse events
def get_color(event, x, y, flags, param):
    global clicked, r, g, b, color_name
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked = True
        b, g, r = map(int, frame[y, x])  # Get RGB color
        color_name = get_color_name(r, g, b)  # Get the name of the color

# Initialize variables
clicked = False
r = g = b = 0
color_name = "Unknown"

# Open webcam
cap = cv2.VideoCapture(0)
cv2.namedWindow("Webcam Feed")
cv2.setMouseCallback("Webcam Feed", get_color)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame. Exiting.")
        break

    # Display the detected color name, RGB values, and color
    if clicked:
        text = f"{color_name} (R: {r}, G: {g}, B: {b})"
        cv2.putText(frame, text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.rectangle(frame, (10, 70), (110, 130), (b, g, r), -1)  # Show detected color

    # Show the live video feed
    cv2.imshow("Webcam Feed", frame)

    # Quit with 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
