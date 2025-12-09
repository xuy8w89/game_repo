import displayio

class Pipe:

    def __init__(self, x, gap_y, gap_h, screen_h, palette, width = 5):
        self.gap_y = gap_y
        self.gap_h = gap_h
        self.screen_h = screen_h
        self.PIPE_WIDTH = width
        self.passed = False

        top_h = gap_y
        self.top_bitmap = displayio.Bitmap(self.PIPE_WIDTH, top_h, 2)

        bottom_h = screen_h - (gap_y + gap_h)
        self.bottom_bitmap = displayio.Bitmap(self.PIPE_WIDTH, bottom_h, 2)

        for x_ in range(self.PIPE_WIDTH):
            for y_ in range(top_h):
                self.top_bitmap[x_, y_] = 1
            for y_ in range(bottom_h):
                self.bottom_bitmap[x_, y_] = 1

        self.top = displayio.TileGrid(
            self.top_bitmap,
            pixel_shader=palette,
            x=x,
            y=0
        )

        self.bottom = displayio.TileGrid(
            self.bottom_bitmap,
            pixel_shader=palette,
            x=x,
            y=gap_y + gap_h
        )

    def move(self, speed):
        self.top.x -= speed
        self.bottom.x -= speed

    def is_off_screen(self):
        return self.top.x < -self.PIPE_WIDTH

    def collides_with(self, ball):
        if ball.collides_with_rect(
            self.top.x, 0,
            self.PIPE_WIDTH, self.gap_y
        ):
            return True

        bottom_y = self.gap_y + self.gap_h
        bottom_h = self.screen_h - bottom_y
        if ball.collides_with_rect(
            self.bottom.x, bottom_y,
            self.PIPE_WIDTH, bottom_h
        ):
            return True

        return False

    def passed_by(self, ball):
        if not self.passed and self.top.x + self.PIPE_WIDTH < ball.x:
            self.passed = True
            return True
        return False
