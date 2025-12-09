import board
import neopixel

class FiveLEDs:
    
    COLORS = {
        1: (255, 0, 0),   
        2: (255, 255, 0), 
        3: (0, 255, 0),   
        0: (0, 0, 0)      
    }

    def __init__(self, pin, num_pixels=5, brightness=0.3):
        self.num_pixels = num_pixels
        self.pixels = neopixel.NeoPixel(pin, num_pixels, brightness=brightness, auto_write=False)
        self.state = [0] * num_pixels  
        self.reset()  

    def reset(self):
        """把所有灯关闭"""
        self.pixels.fill(self.COLORS[0])
        self.pixels.show()
        self.state = [0] * self.num_pixels

    def set_light(self, index, color_index):
        """设置单个灯的颜色"""
        if 0 <= index < self.num_pixels and color_index in self.COLORS:
            if self.state[index] != color_index:  
                self.pixels[index] = self.COLORS[color_index]
                self.pixels.show()
                self.state[index] = color_index

    def set_lights(self, color_list):
        need_update = False
        for i, color_index in enumerate(color_list):
            if self.state[i] != color_index:
                self.pixels[i] = self.COLORS[color_index]
                self.state[i] = color_index
                need_update = True

        if need_update:
            self.pixels.show()  

if __name__ == "__main__":
    led_strip = FiveLEDs(board.D10)
    
    led_strip.set_lights((1, 2, 3, 0)) 
    led_strip.set_lights((1, 2, 3, 0))
