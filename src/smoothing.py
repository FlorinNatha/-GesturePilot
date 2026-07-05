class CursorSmoother:
    def __init__(self, smoothing_factor=0.3):
        self.prev_x = 0
        self.prev_y = 0
        self.smoothing_factor = smoothing_factor

    def smooth(self, current_x, current_y):
        if self.prev_x == 0 and self.prev_y == 0:
            self.prev_x = current_x
            self.prev_y = current_y
            
        smoothed_x = self.prev_x + (current_x - self.prev_x) * self.smoothing_factor
        smoothed_y = self.prev_y + (current_y - self.prev_y) * self.smoothing_factor
        
        self.prev_x = smoothed_x
        self.prev_y = smoothed_y
        
        return int(smoothed_x), int(smoothed_y)
