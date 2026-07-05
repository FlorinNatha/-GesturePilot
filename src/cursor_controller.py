import pyautogui
from src import config

# Optional: Disable failsafe if it gets annoying during testing
pyautogui.FAILSAFE = False

class CursorController:
    def move(self, x, y):
        """
        Move the cursor to the specified screen coordinates safely.
        """
        # Ensure coordinates are within screen boundaries
        x = max(0, min(config.SCREEN_WIDTH - 1, x))
        y = max(0, min(config.SCREEN_HEIGHT - 1, y))
        pyautogui.moveTo(x, y)
