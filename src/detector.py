import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from src import config

HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4), # Thumb
    (0, 5), (5, 6), (6, 7), (7, 8), # Index finger
    (5, 9), (9, 10), (10, 11), (11, 12), # Middle finger
    (9, 13), (13, 14), (14, 15), (15, 16), # Ring finger
    (13, 17), (0, 17), (17, 18), (18, 19), (19, 20) # Pinky and palm base
]

class HandDetector:
    def __init__(self):
        base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=config.MAX_NUM_HANDS,
            min_hand_detection_confidence=config.MIN_DETECTION_CONFIDENCE,
            min_hand_presence_confidence=config.MIN_TRACKING_CONFIDENCE,
            min_tracking_confidence=config.MIN_TRACKING_CONFIDENCE
        )
        self.detector = vision.HandLandmarker.create_from_options(options)
        self.results = None

    def find_hands(self, img, draw=True):
        """
        Detect hands in the given image using MediaPipe Tasks API.
        """
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)
        
        self.results = self.detector.detect(mp_image)
        
        if self.results.hand_landmarks and draw:
            for hand_landmarks in self.results.hand_landmarks:
                h, w, c = img.shape
                
                # Draw connections
                for connection in HAND_CONNECTIONS:
                    start_idx = connection[0]
                    end_idx = connection[1]
                    lm1 = hand_landmarks[start_idx]
                    lm2 = hand_landmarks[end_idx]
                    
                    x1, y1 = int(lm1.x * w), int(lm1.y * h)
                    x2, y2 = int(lm2.x * w), int(lm2.y * h)
                    
                    cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 2)
                    
                # Draw landmarks
                for lm in hand_landmarks:
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
                    
        return img, self.results
        
    def get_landmarks(self, img):
        """
        Extract landmark positions for the first detected hand.
        Returns a list of dictionaries with id, cx, cy coordinates, and normalized x, y, z.
        """
        landmarks = []
        if self.results and self.results.hand_landmarks:
            my_hand = self.results.hand_landmarks[0]
            h, w, c = img.shape
            for id, lm in enumerate(my_hand):
                cx, cy = int(lm.x * w), int(lm.y * h)
                landmarks.append({
                    'id': id,
                    'cx': cx,
                    'cy': cy,
                    'norm_x': lm.x,
                    'norm_y': lm.y,
                    'norm_z': lm.z
                })
        return landmarks
