import cv2
import numpy as np

def camera_with_invisibility_cloak():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    print("Press 'c' to capture the background, 'q' to quit.")

    background = None
    background_captured = False

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        if background is not None:
            # Convert the frame to the HSV color space
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # Define the range of color to be considered as "invisible"
            # For example, use green color to make it "invisible"
            lower_green = np.array([40, 40, 40])  
            upper_green = np.array([100, 255, 255])

            # Create a mask for the color range (invisible color)
            mask = cv2.inRange(hsv, lower_green, upper_green)
            mask_inv = cv2.bitwise_not(mask)
            
            background_part = cv2.bitwise_and(background, background, mask=mask)
            frame_part = cv2.bitwise_and(frame, frame, mask=mask_inv)
            combined_frame = cv2.add(background_part, frame_part)
            cv2.imshow('Camera Feed with Invisibility Cloak', combined_frame)
        else:
            cv2.imshow('Camera Feed', frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('c') and not background_captured:
            background = frame.copy()
            background_captured = True
            print("Background captured.")

        elif key == ord('q'):
            print("Exiting...")
            break

    # Release the camera and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    camera_with_invisibility_cloak()