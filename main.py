import cv2
import time
import numpy as np
from src.detector import HandDetector
from src.gesture_recognizer import GestureRecognizer
from src.cursor_controller import CursorController
from src.drag_controller import DragController
from src.smoothing import CursorSmoother
from src import config

def main():
    cap = cv2.VideoCapture(config.CAMERA_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAMERA_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAMERA_HEIGHT)
    
    detector = HandDetector()
    recognizer = GestureRecognizer()
    
    # Initialize Automation Controllers
    cursor = CursorController()
    dragger = DragController()
    smoother = CursorSmoother(smoothing_factor=0.2)
    
    pTime = 0
    
    print("Starting GesturePilot... Press 'q' to exit.")
    
    while True:
        success, img = cap.read()
        if not success:
            print("Failed to read from camera. Exiting...")
            break
            
        # Flip the image horizontally for a natural mirror effect
        img = cv2.flip(img, 1)
        
        # Detect hands and draw landmarks
        img, results = detector.find_hands(img)
        landmarks = detector.get_landmarks(img)
        
        # Calculate and display FPS
        cTime = time.time()
        fps = 1 / (cTime - pTime) if (cTime - pTime) > 0 else 0
        pTime = cTime
        
        cv2.putText(img, f'FPS: {int(fps)}', (10, 50), 
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
                    
        # Gesture Recognition & Automation
        if landmarks:
            gesture = recognizer.recognize(landmarks)
            cv2.putText(img, f'Gesture: {gesture}', (10, 100), 
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
                        
            # Get Index Finger Tip Coordinates
            index_x = landmarks[8]['cx']
            index_y = landmarks[8]['cy']
            
            # Interpolate coordinates to screen size
            # Since camera feed is horizontally flipped, we might need to map it carefully,
            # but since we flip the image earlier, index_x is already correct visually.
            screen_x = np.interp(index_x, (0, config.CAMERA_WIDTH), (0, config.SCREEN_WIDTH))
            screen_y = np.interp(index_y, (0, config.CAMERA_HEIGHT), (0, config.SCREEN_HEIGHT))
            
            # Smooth the movement to prevent jitter
            smooth_x, smooth_y = smoother.smooth(screen_x, screen_y)
            
            # State Machine Actions
            if gesture == "Index_Up":
                cursor.move(smooth_x, smooth_y)
                dragger.stop_drag()
                
            elif gesture == "Pinch":
                # Quick pinch naturally performs a click. Sustained pinch performs click and drag.
                cursor.move(smooth_x, smooth_y)
                dragger.start_drag()
                
            elif gesture == "Open_Palm":
                # Pause / Ignore commands
                dragger.stop_drag()
                cv2.putText(img, "PAUSED", (config.CAMERA_WIDTH - 200, 50), 
                            cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
                            
            elif gesture == "Closed_Fist":
                # Safe exit
                dragger.stop_drag()
                print("Closed Fist detected. Exiting gracefully...")
                break
            else:
                # For Peace/Zoom or unhandled, just release the drag to be safe
                dragger.stop_drag()
                    
        cv2.imshow("GesturePilot Tracking", img)
        
        # Exit condition
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
