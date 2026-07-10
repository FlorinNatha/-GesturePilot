import time
from src.utils import calculate_distance

class GestureRecognizer:
    def __init__(self):
        # MediaPipe landmark IDs for finger tips
        # Thumb: 4, Index: 8, Middle: 12, Ring: 16, Pinky: 20
        self.TIP_IDS = [4, 8, 12, 16, 20]
        self.current_gesture = "None"
        self.previous_gesture = "None"
        self.last_gesture_time = 0
        self.gesture_cooldown = 0.5 # Seconds
        
    def fingers_up(self, landmarks):
        """
        Determine which fingers are extended.
        Returns a list of 5 integers (1 for up, 0 for down) for [Thumb, Index, Middle, Ring, Pinky].
        """
        fingers = []
        if not landmarks or len(landmarks) < 21:
            return [0, 0, 0, 0, 0]
            
        # 1. Thumb
        # Compare distance from Thumb Tip (4) to Pinky Base (17) 
        # vs Thumb IP Joint (3) to Pinky Base (17). If tip is further, it's extended.
        dist_tip = calculate_distance((landmarks[4]['cx'], landmarks[4]['cy']), 
                                      (landmarks[17]['cx'], landmarks[17]['cy']))
        dist_joint = calculate_distance((landmarks[3]['cx'], landmarks[3]['cy']), 
                                        (landmarks[17]['cx'], landmarks[17]['cy']))
        if dist_tip > dist_joint:
            fingers.append(1)
        else:
            fingers.append(0)
            
        # 2. Four Fingers
        # Compare y coordinates. If tip y is lower than PIP joint y (lower y means higher on screen)
        for id in range(1, 5):
            if landmarks[self.TIP_IDS[id]]['cy'] < landmarks[self.TIP_IDS[id] - 2]['cy']:
                fingers.append(1)
            else:
                fingers.append(0)
                
        return fingers

    def get_pinch_distance(self, landmarks):
        """
        Calculate the distance between thumb tip and index tip.
        """
        if not landmarks or len(landmarks) < 21:
            return 0.0, None, None
            
        thumb_tip = (landmarks[4]['cx'], landmarks[4]['cy'])
        index_tip = (landmarks[8]['cx'], landmarks[8]['cy'])
        
        distance = calculate_distance(thumb_tip, index_tip)
        return distance, thumb_tip, index_tip

    def get_middle_pinch_distance(self, landmarks):
        """
        Calculate the distance between thumb tip and middle finger tip for Right Click.
        """
        if not landmarks or len(landmarks) < 21:
            return 0.0
            
        thumb_tip = (landmarks[4]['cx'], landmarks[4]['cy'])
        middle_tip = (landmarks[12]['cx'], landmarks[12]['cy'])
        
        return calculate_distance(thumb_tip, middle_tip)

    def recognize(self, landmarks):
        """
        Identify the current gesture based on landmarks and fingers up.
        Returns the recognized gesture as a string.
        """
        if not landmarks:
            return "None"
            
        fingers = self.fingers_up(landmarks)
        pinch_dist, _, _ = self.get_pinch_distance(landmarks)
        middle_pinch_dist = self.get_middle_pinch_distance(landmarks)
        
        raw_gesture = "None"
        
        # State Machine Logic
        
        # 1. Pinch Gesture (Left Click - Thumb and Index close)
        # Relaxed threshold to 60, and removed strict checking for other fingers to make it much easier to trigger.
        if pinch_dist < 60:
            raw_gesture = "Pinch"
            
        # 1.5 Right Click (Thumb and Middle close)
        elif middle_pinch_dist < 60 and fingers[1] == 1:
            raw_gesture = "Right_Click"
            
        # 2. Open Palm (All fingers up)
        elif fingers == [1, 1, 1, 1, 1]:
            raw_gesture = "Open_Palm"
            
        # 3. Closed Fist (All fingers down)
        elif fingers == [0, 0, 0, 0, 0] or fingers[1:] == [0, 0, 0, 0]:
            raw_gesture = "Closed_Fist"
            
        # 4. Peace / Zoom (Index and Middle up, others down)
        elif fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
            raw_gesture = "Peace"
            
        # 5. Index Up (Only Index finger up)
        elif fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
            raw_gesture = "Index_Up"
            
        # Apply Cooldown state management
        current_time = time.time()
        
        # If the gesture changed, check if cooldown has passed
        if raw_gesture != self.current_gesture:
            if (current_time - self.last_gesture_time) > self.gesture_cooldown:
                self.previous_gesture = self.current_gesture
                self.current_gesture = raw_gesture
                self.last_gesture_time = current_time
        
        return self.current_gesture
