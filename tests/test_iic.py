import board
import busio
import displayio
import terminalio
from adafruit_display_text import label
import i2cdisplaybus
import adafruit_displayio_ssd1306

# Release any currently active displays
# ensures no conflict with existing display
displayio.release_displays()

# Create an I2C bus connection.
# board.SCL is the clock line, and board.SDA is the data line.
# tells mcu how to manipulate on SCL and SDA
i2c = busio.I2C(board.SCL, board.SDA)

# Create an I2C display bus for the SSD1306 display.
# device_address=0x3C is the common I2C address for most SSD1306 OLEDs.
# multiple I2C devices can be driven by single i2c
display_bus = i2cdisplaybus.I2CDisplayBus(i2c, device_address=0x3C)

# Create the SSD1306 display object.
# width and height specify the resolution of the display in pixels.
# This object manages all drawing operations to the OLED.
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)

# Create a group object as the container for visual elements.
# A Group can hold multiple layers and multiple objects (text, shapes, images, etc.).
main_group = displayio.Group()

# Create a text label to display on the screen.
# terminalio.FONT is a built-in monospaced font.
# The 'text' argument defines what text will be shown.
# x and y set the position of the top-left corner of the text (in pixels).
text_layer = label.Label(terminalio.FONT, text="Hello Weiye!", x=30, y=30)

# Add the text layer to the display group.
# The Group keeps track of all visual elements, and append() adds this one to the list.
# also, all these layers are visualize in a sequential way, which means that the later one will appear on topper place.
main_group.append(text_layer)

# Set the display’s root group to the one you created.
# The "root_group" is what actually gets drawn to the screen.
# Whatever you assign to display.root_group becomes visible on the OLED.
display.root_group = main_group