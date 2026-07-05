import cv2
import mediapipe as mp
from src import config

class HandDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=config.MAX_NUM_HANDS,
            min_detection_confidence=config.MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=config.MIN_TRACKING_CONFIDENCE
        )
        self.mp_draw = mp.solutions.drawing_utils
        
    def find_hands(self, img, draw=True):
        """
        Detect hands in the given image.
        Returns the image (optionally with landmarks drawn) and the raw results.
        """
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        
        if self.results.multi_hand_landmarks and draw:
            for hand_landmarks in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    img, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                    
        return img, self.results
        
    def get_landmarks(self, img):
        """
        Extract landmark positions for the first detected hand.
        Returns a list of dictionaries with id, cx, cy coordinates, and normalized x, y, z.
        """
        landmarks = []
        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[0]
            h, w, c = img.shape
            for id, lm in enumerate(my_hand.landmark):
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
