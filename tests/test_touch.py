import board
import analogio
import time

class TouchButton:
    def __init__(self, pin, threshold=3000):
        """
        pin: analog pin for touch input (board.TOUCH0, etc.)
        threshold: value below which is considered 'pressed'
        """
        self.analog = analogio.AnalogIn(pin)
        self.threshold = threshold
        self._was_pressed = False

    def is_pressed(self):
        value = self.analog.value
        print(value)
        return value < self.threshold

    def was_pressed(self):
        pressed = self.is_pressed()
        if pressed and not self._was_pressed:
            self._was_pressed = True
            return True
        elif not pressed:
            self._was_pressed = False
        return False

# ======================
# Example
# ======================
