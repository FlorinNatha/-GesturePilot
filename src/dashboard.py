import cv2

class Dashboard:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
    def draw(self, img, fps, gesture, is_paused):
        """
        Draw a stylish HUD overlay on the image.
        """
        # Create a dark semi-transparent top bar
        overlay = img.copy()
        cv2.rectangle(overlay, (0, 0), (self.width, 80), (30, 30, 30), -1)
        # Apply the overlay with alpha blending
        cv2.addWeighted(overlay, 0.6, img, 0.4, 0, img)
        
        # System State (Top Right)
        state_color = (0, 0, 255) if is_paused else (0, 255, 0)
        state_text = "PAUSED" if is_paused else "ACTIVE"
        
        # Draw bounding box for state
        cv2.rectangle(img, (self.width - 160, 20), (self.width - 20, 60), state_color, 2)
        cv2.putText(img, state_text, (self.width - 140, 48), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, state_color, 2)
                    
        # FPS Counter (Top Left)
        # Color codes based on FPS health
        fps_color = (0, 255, 0) if fps > 20 else (0, 165, 255) if fps > 10 else (0, 0, 255)
        cv2.putText(img, f"FPS: {int(fps)}", (20, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, fps_color, 2)
                    
        # Active Gesture (Center)
        # Nice vibrant blue/gold color
        cv2.putText(img, f"GESTURE: {gesture}", (250, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 200, 0), 2)
                    
        return img
