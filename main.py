import cv2
import time
from src.detector import HandDetector
from src.gesture_recognizer import GestureRecognizer
from src import config

def main():
    cap = cv2.VideoCapture(config.CAMERA_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAMERA_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAMERA_HEIGHT)
    
    detector = HandDetector()
    recognizer = GestureRecognizer()
    
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
                    
        # Gesture Recognition
        if landmarks:
            gesture = recognizer.recognize(landmarks)
            cv2.putText(img, f'Gesture: {gesture}', (10, 100), 
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
                    
        cv2.imshow("GesturePilot Tracking", img)
        
        # Exit condition
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
