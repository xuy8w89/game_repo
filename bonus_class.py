import displayio

class Bonus:
    def __init__(self, x, y, radius=6, btype="sk_hold"):
        self.radius = radius
        self.x = float(x)
        self.y = float(y)
        size = radius * 2
        self.bitmap = displayio.Bitmap(size, size, 2)
        self.palette = displayio.Palette(2)
        self.palette[0] = 0x000000
        self.palette[1] = 0xFFFFFF
        self.btype = btype

        for py in range(size):
            for px in range(size):
                if (px - radius) ** 2 + (py - radius) ** 2 <= radius ** 2 and (px - radius) ** 2 + (py - radius) ** 2 >= radius ** 2 /4:
                    self.bitmap[px, py] = 1

        self.sprite = displayio.TileGrid(
            self.bitmap,
            pixel_shader=self.palette,
            x=int(self.x - self.radius),
            y=int(self.y - self.radius)
        )

    def eaten_by(self, ball):
        if ball.collides_with_ball(
            self.x, self.y, self.radius
        ):
            return True
        return False

    def move(self, speed):
        self.sprite.x -= speed
        self.x -= speed

    def is_off_screen(self):
        return self.x < -2 * self.radius