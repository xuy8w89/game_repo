import board
import time
import adafruit_adxl34x
import busio
import displayio
import terminalio
import i2cdisplaybus
import adafruit_displayio_ssd1306
from adafruit_display_text import label

i2c = busio.I2C(board.SCL, board.SDA)

accelerometer = adafruit_adxl34x.ADXL345(i2c)

while True:
    print("{} {} {}".format(*accelerometer.acceleration))
    time.sleep(0.4)