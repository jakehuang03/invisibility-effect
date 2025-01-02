import cv2
import numpy as np

# Global variable to store the selected color
selected_color = None

def mouse_callback(event, x, y, flags, frame):
    global selected_color  # Use the global selected_color
    if event == cv2.EVENT_LBUTTONDOWN:
        # Get the BGR color at the pixel
        bgr_color = frame[y, x]
        # Convert the BGR color to HSV
        hsv_color = cv2.cvtColor(np.uint8([[bgr_color]]), cv2.COLOR_BGR2HSV)
        selected_color = tuple(int(c) for c in bgr_color)
        print(f"Selected color (HSV): {selected_color}")

cv2.namedWindow("image")

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    # If a color is selected, draw a small rectangle at the top-left corner
    if selected_color is not None:
        cv2.rectangle(frame, (10, 10), (160, 60), selected_color, -1)

    # Set mouse callback to detect color2346
    cv2.setMouseCallback("image", mouse_callback, frame)

    # Display the frame
    cv2.imshow("image", frame)

    # Press 'q' to quit
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()