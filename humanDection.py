import cv2
import time
import mediapipe as mp

face_dection = True
def mouse_callback(event, x, y, flags, param):
    global face_dection
    if event == cv2.EVENT_LBUTTONDOWN:
        if 20 <= x <= 150 and 50 <= y <= 100:  
            face_dection = not face_dection
            print(f"Face detection {'enabled' if face_dection else 'disabled'}")

mp_holistic = mp.solutions.holistic
holistic_model = mp_holistic.Holistic(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

mp_drawing = mp.solutions.drawing_utils
capture = cv2.VideoCapture(0)
 
previousTime = 0
currentTime = 0
 
while capture.isOpened():
    # capture frame by frame
    ret, frame = capture.read()
    cv2.setMouseCallback("Facial and Hand Landmarks", mouse_callback)

    image = frame.copy()
    if face_dection:
  
      image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
      # Making predictions using holistic model
      # To improve performance, optionally mark the image as not writeable to
      # pass by reference.
      image.flags.writeable = False
      results = holistic_model.process(image)
      image.flags.writeable = True
  
      # Converting back the RGB image to BGR
      image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
  
      # Drawing the Facial Landmarks
      mp_drawing.draw_landmarks(
        image,
        results.face_landmarks,
        mp_holistic.FACEMESH_TESSELATION,
        mp_drawing.DrawingSpec(
          color=(255,0,255),
          thickness=1,
          circle_radius=1
        ),
        mp_drawing.DrawingSpec(
          color=(0,255,255),
          thickness=1,
          circle_radius=1
        )
      )
  
      # Drawing Right hand Land Marks
      mp_drawing.draw_landmarks(
        image, 
        results.right_hand_landmarks, 
        mp_holistic.HAND_CONNECTIONS
      )
  
      # Drawing Left hand Land Marks
      mp_drawing.draw_landmarks(
        image, 
        results.left_hand_landmarks, 
        mp_holistic.HAND_CONNECTIONS
      )

    button_color = (0, 255, 0) if face_dection else (0, 0, 255)
    cv2.rectangle(image, (20, 50), (150, 100), button_color, -1)
    button_text = "ON" if face_dection else "OFF"
    cv2.putText(image, f"Face Detection: {button_text}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # Display the resulting image
    cv2.imshow("Facial and Hand Landmarks", image)
 
    # Enter key 'q' to break the loop
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break
 
capture.release()
cv2.destroyAllWindows()