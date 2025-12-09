# finish_line.py
import displayio

class FinishLine:
    def __init__(self, x, screen_h=64):
        self.bitmap = displayio.Bitmap(4, screen_h, 2)
        self.palette = displayio.Palette(2)
        self.palette[0] = 0x000000
        self.palette[1] = 0xFFFFFF

        # 画“终点虚线（更粗）”
        for y in range(0, screen_h, 3):
            for w in range(4):
                self.bitmap[w, y] = 1

        self.sprite = displayio.TileGrid(
            self.bitmap,
            pixel_shader=self.palette,
            x=x,
            y=0
        )

    def move(self, speed):
        self.sprite.x -= speed

    def is_off_screen(self):
        return self.sprite.x < -4

    def collides_with(self, bird):
        bx = bird.sprite.x
        if abs(self.sprite.x - bx) < 4:
            return True
        return False
