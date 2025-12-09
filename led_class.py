import board
import neopixel

class FiveLEDs:
    # 定义颜色
    COLORS = {
        1: (255, 0, 0),   # 红色
        2: (255, 255, 0), # 黄色
        3: (0, 255, 0),   # 绿色
        0: (0, 0, 0)      # 关闭
    }

    def __init__(self, pin, num_pixels=5, brightness=0.3):
        self.num_pixels = num_pixels
        self.pixels = neopixel.NeoPixel(pin, num_pixels, brightness=brightness, auto_write=False)
        self.state = [0] * num_pixels  # 当前每个灯的color_index，初始化为关闭
        self.reset()  # 初始化时全部关闭

    def reset(self):
        """把所有灯关闭"""
        self.pixels.fill(self.COLORS[0])
        self.pixels.show()
        self.state = [0] * self.num_pixels

    def set_light(self, index, color_index):
        """设置单个灯的颜色"""
        if 0 <= index < self.num_pixels and color_index in self.COLORS:
            if self.state[index] != color_index:  # 如果状态相同则不操作
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
            self.pixels.show()  # 只有状态发生变化才刷新

# ------------------ 示例用法 ------------------
if __name__ == "__main__":
    led_strip = FiveLEDs(board.D10)
    
    # 一次性设置前4个灯
    led_strip.set_lights((1, 2, 3, 0))  # 红, 黄, 绿, 关闭
    # 再次调用相同状态，不会刷新
    led_strip.set_lights((1, 2, 3, 0))
