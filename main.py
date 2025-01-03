import cv2
import numpy as np

selected_color_hsv = None

def mouse_callback(event, x, y, flags, frame):
    global selected_color_hsv
    if event == cv2.EVENT_LBUTTONDOWN:
        bgr_color = frame[y, x]
        hsv_color = cv2.cvtColor(np.uint8([[bgr_color]]), cv2.COLOR_BGR2HSV)
        selected_color_hsv = tuple(int(c) for c in hsv_color[0][0])
        print(f"hsv: {selected_color_hsv}")
def camera_with_invisibility_cloak():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    print("Press 'c' to capture the background, 'q' to quit.")
    print("Click on the color in the video feed to select it for invisibility.")
    print("Default color for invisibility is cyan if no color is selected.")

    background = None
    background_captured = False

    while True:
        ret, frame = cap.read()
        cv2.namedWindow("Camera Feed")
        cv2.setMouseCallback("Camera Feed", mouse_callback, frame)

        if not ret:
            print("Failed to grab frame.")
            break
        
        if background is not None:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            if selected_color_hsv is not None:
                lower_bound = np.array([
                    max(0, selected_color_hsv[0] - 25),  
                    max(0, selected_color_hsv[1] - 60),  
                    max(0, selected_color_hsv[2] - 60)   
                ])
                upper_bound = np.array([
                    min(179, selected_color_hsv[0] + 25),  
                    min(255, selected_color_hsv[1] + 60),  
                    min(255, selected_color_hsv[2] + 60)   
                ])  
            else:         
                lower_bound = np.array([40, 40, 40])  
                upper_bound = np.array([100, 255, 255])

            lower_bound_bgr = cv2.cvtColor(np.uint8([[lower_bound]]), cv2.COLOR_HSV2BGR)[0][0]
            lower_bound_bgr = tuple(int(c) for c in lower_bound_bgr)
            upper_bound_bgr = cv2.cvtColor(np.uint8([[upper_bound]]), cv2.COLOR_HSV2BGR)[0][0]
            upper_bound_bgr = tuple(int(c) for c in upper_bound_bgr)

            # Draw rectangles for the bounds
            cv2.rectangle(frame, (10, 10), (80, 60), lower_bound_bgr, -1)  
            cv2.rectangle(frame, (90, 10), (160, 60), upper_bound_bgr, -1)
            
            # Create a mask for the color range (invisible color)
            mask = cv2.inRange(hsv, lower_bound, upper_bound)
            mask_inv = cv2.bitwise_not(mask)
            
            background_part = cv2.bitwise_and(background, background, mask=mask)
            frame_part = cv2.bitwise_and(frame, frame, mask=mask_inv)
            combined_frame = cv2.add(background_part, frame_part)
            cv2.imshow('Camera Feed with Invisibility Cloak', combined_frame)
        else:
            if selected_color_hsv is not None:
                selected_color_bgr = cv2.cvtColor(np.uint8([[selected_color_hsv]]), cv2.COLOR_HSV2BGR)[0][0]
                selected_color_bgr = tuple(int(c) for c in selected_color_bgr)
                cv2.rectangle(frame, (10, 10), (160, 60), selected_color_bgr, -1)
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