import pyautogui

class DragController:
    def __init__(self):
        self.is_dragging = False
        
    def start_drag(self):
        if not self.is_dragging:
            pyautogui.mouseDown()
            self.is_dragging = True
            
    def stop_drag(self):
        if self.is_dragging:
            pyautogui.mouseUp()
            self.is_dragging = False
