import displayio

class Ball:
    def __init__(self, x, y, radius=4, gravity=0.6):
        self.radius = radius
        self.x = float(x)
        self.y = float(y)

        self.vy = 0.0
        self.gravity = gravity

        size = radius * 2
        self.bitmap = displayio.Bitmap(size, size, 2)
        self.palette = displayio.Palette(2)
        self.palette[0] = 0x000000
        self.palette[1] = 0xFFFFFF

        for py in range(size):
            for px in range(size):
                if (px - radius) ** 2 + (py - radius) ** 2 <= radius ** 2:
                    self.bitmap[px, py] = 1

        self.sprite = displayio.TileGrid(
            self.bitmap,
            pixel_shader=self.palette,
            x=int(self.x - self.radius),
            y=int(self.y - self.radius)
        )
        
        self.bitmap_2 = displayio.Bitmap(size, size, 2)
        for py in range(size):
            for px in range(size):
                if (px + py) % 4 == 0 and (px - radius) ** 2 + (py - radius) ** 2 <= radius ** 2:
                    self.bitmap_2[px, py] = 1

        self.sprite = displayio.TileGrid(
            self.bitmap,
            pixel_shader=self.palette,
            x=int(self.x - self.radius),
            y=int(self.y - self.radius)
        )
        
        self.vis_2 = displayio.TileGrid(
            self.bitmap_2,
            pixel_shader=self.palette,
            x = 0,
            y = 0,
        )

    def lock_to_spawn(self):
        self.velocity = 0
        self.vis_2.x = self.sprite.x
        self.vis_2.y = self.sprite.y

    def jump(self, strength=7):
        self.vy = -strength

    def update(self, screen_h):
        self.vy += self.gravity
        self.y += self.vy

        if self.y <= self.radius:
            self.y = self.radius
            self.vy = 0

        if self.y >= screen_h - self.radius:
            self.y = screen_h - self.radius
            self.vy = 0

        self.sprite.y = int(self.y - self.radius)

    def get_bbox(self):
        return (
            self.x - self.radius,
            self.y - self.radius,
            self.x + self.radius,
            self.y + self.radius
        )

    def collides_with_rect(self, rx, ry, rw, rh):
        ax1, ay1, ax2, ay2 = self.get_bbox()
        bx1, by1, bx2, by2 = rx, ry, rx + rw, ry + rh
        return not (ax2 <= bx1 or ax1 >= bx2 or ay2 <= by1 or ay1 >= by2)
    
    def collides_with_ball(self, x, y, r):
        if (y - self.y)**2 + (x - self.x)**2 <= (r + self.radius)**2:
            return True
        return False
