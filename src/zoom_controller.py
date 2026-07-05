import pyautogui
import time

class ZoomController:
    def __init__(self):
        self.last_action_time = 0
        self.cooldown = 0.2
        
    def zoom_in(self):
        current_time = time.time()
        if (current_time - self.last_action_time) > self.cooldown:
            pyautogui.scroll(200) # Positive is scroll up
            self.last_action_time = current_time
            
    def zoom_out(self):
        current_time = time.time()
        if (current_time - self.last_action_time) > self.cooldown:
            pyautogui.scroll(-200) # Negative is scroll down
            self.last_action_time = current_time
