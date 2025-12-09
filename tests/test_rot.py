import time
import board
import busio
import displayio
import terminalio
import i2cdisplaybus
import adafruit_displayio_ssd1306
from adafruit_display_text import label
from rotary_encoder import RotaryEncoder


# Rotary encoder setup
encoder = RotaryEncoder(board.D3, board.D2, debounce_ms=3, pulses_per_detent=3)

def translate(number: int):
    i = number % 26
    return chr(ord('A')+i)

# Main loop
while True:
    if encoder.update():
        print(f"Position: {translate(encoder.position)}")
    time.sleep(0.01)