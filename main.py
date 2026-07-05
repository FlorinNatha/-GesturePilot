import cv2
import time
import numpy as np
from src.detector import HandDetector
from src.gesture_recognizer import GestureRecognizer
from src.cursor_controller import CursorController
from src.drag_controller import DragController
from src.zoom_controller import ZoomController
from src.smoothing import CursorSmoother
from src.utils import calculate_distance
from src.dashboard import Dashboard
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
    zoomer = ZoomController()
    smoother = CursorSmoother(smoothing_factor=0.2)
    dashboard = Dashboard(config.CAMERA_WIDTH, config.CAMERA_HEIGHT)
    
    pTime = 0
    prev_zoom_dist = 0
    fist_time = 0
    last_right_click_time = 0
    
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
        
        # State tracking
        current_gesture = "None"
        is_paused = False
                    
        # Gesture Recognition & Automation
        if landmarks:
            current_gesture = recognizer.recognize(landmarks)
                        
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
            if current_gesture == "Index_Up":
                cursor.move(smooth_x, smooth_y)
                dragger.stop_drag()
                
            elif current_gesture == "Pinch":
                # Quick pinch naturally performs a click. Sustained pinch performs click and drag.
                cursor.move(smooth_x, smooth_y)
                dragger.start_drag()
                
            elif current_gesture == "Right_Click":
                # Move cursor and right click (with cooldown)
                cursor.move(smooth_x, smooth_y)
                dragger.stop_drag()
                if time.time() - last_right_click_time > 1.0:
                    import pyautogui
                    pyautogui.rightClick()
                    last_right_click_time = time.time()
                
            elif current_gesture == "Open_Palm":
                # Pause / Ignore commands
                dragger.stop_drag()
                is_paused = True
                            
            elif current_gesture == "Closed_Fist":
                # Safe exit requires holding for 2 seconds to prevent accidental closing
                dragger.stop_drag()
                if fist_time == 0:
                    fist_time = time.time()
                elif time.time() - fist_time > 2.0:
                    print("Closed Fist held for 2 seconds. Exiting gracefully...")
                    break
                else:
                    cv2.putText(img, "Hold Fist to Exit...", (config.CAMERA_WIDTH // 2 - 200, config.CAMERA_HEIGHT // 2), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                
            elif current_gesture == "Peace":
                dragger.stop_drag()
                # Calculate distance between Index (8) and Middle (12)
                idx_x, idx_y = landmarks[8]['cx'], landmarks[8]['cy']
                mid_x, mid_y = landmarks[12]['cx'], landmarks[12]['cy']
                
                zoom_dist = calculate_distance((idx_x, idx_y), (mid_x, mid_y))
                
                if prev_zoom_dist != 0:
                    if zoom_dist > prev_zoom_dist + 5: 
                        zoomer.zoom_in()
                    elif zoom_dist < prev_zoom_dist - 5:
                        zoomer.zoom_out()
                prev_zoom_dist = zoom_dist
                
            else:
                # Unhandled gesture, release drag and reset zoom state
                dragger.stop_drag()
                prev_zoom_dist = 0
                
            # Reset fist timer if not currently making a fist
            if current_gesture != "Closed_Fist":
                fist_time = 0
                
        # Draw UI Dashboard
        img = dashboard.draw(img, fps, current_gesture, is_paused)
                    
        cv2.imshow("GesturePilot Tracking", img)
        
        # Exit condition
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
