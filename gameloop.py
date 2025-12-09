from ball_class import Ball
from pipe_class import Pipe
from bonus_class import Bonus
from finish_line import FinishLine
import displayio
import random, time
import terminalio
import math
from adafruit_display_text import label

def construct_skill_tile():
    width = 20
    height = 64

    radius = 100
    bitmap = displayio.Bitmap(width, height, 2) 
    palette = displayio.Palette(2)
    palette[0] = 0x000000  
    palette[1] = 0xFFFFFF  

    for y in range(height):
        for x in range(width):
            dx = radius - width // 2 + x
            dy = height // 2 - y
            if dx*dx + dy*dy <= radius*radius and dx*dx + dy*dy >= (radius - 5)**2:
                bitmap[x, y] = 1

    tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette, x=0, y=0)
    return tile_grid

class gameloop():
    def __init__(self, main_group):
        self.main_group = main_group

    # =========================
    def wrap_up(self):
        while len(self.main_group) > 0:
            self.main_group.pop()

        self.pipes.clear()
        self.bird = None
        self.bonus = None
        self.finish_line = None
        self.score_label = None
        self.pipe_palette = None 

        
        import gc
        gc.collect()
    
    def init_game(self, mode="Debug"):
        self.killed = False
        self.mode = mode
        self.frame = 0
        self.idle_frame_counter = 0
        self.anime_status = None
        self.skill_status = False
        self.skill_timer = 66
        
        # progress
        self.progress = 0
        self.last_progress_mark = 0

        # -------- bird --------
        self.spawn_x = 30
        self.spawn_y = 32
        self.bird = Ball(self.spawn_x, self.spawn_y)
        self.main_group.append(self.bird.sprite)

        # -------- pipes --------
        self.PIPE_WIDTH = 5
        self.PIPE_GAP = 45
        self.PIPE_SPEED = 2

        self.pipes = []
        self.pipe_palette = displayio.Palette(2)
        self.pipe_palette[0] = 0x000000
        self.pipe_palette[1] = 0xFFFFFF

        # -------- bonus --------
        self.bonus = None
        self.bonus_palette = self.pipe_palette
        self.bonus_palette[0] = 0x000000
        self.bonus_palette[1] = 0xFFFFFF
        self.bonus_thresh = 5
        
        # finish_line
        self.finish_line = None

        # score
        self.score = 0
        self.gameover = False
        self.finished = False 

        # game_settings
        if mode == "Easy":
            self.target_pipes = 20
            self.progress_step = 2
            self.skill = 1
            self.life = 3
        elif mode == "Normal":
            self.target_pipes = 20
            self.progress_step = 2
            self.PIPE_GAP -= 5
            self.PIPE_WIDTH += 2
            self.bonus_thresh -= 2
            self.skill = 0
            self.life = 2
        elif mode == "Hard":
            self.target_pipes = 30
            self.progress_step = 3
            self.PIPE_GAP -= 5
            self.PIPE_WIDTH += 5
            self.bonus_thresh -= 4
            self.skill = 0
            self.life = 1
        else:
            self.target_pipes = None   # infinite
            self.progress_step = None
            self.PIPE_GAP -= 10
            self.PIPE_WIDTH += 2
            self.bonus_thresh -= 2
            self.skill = 0
            self.life = 2
        
        # display
        self.score_label = label.Label(
            terminalio.FONT,
            text="Score: 0",
            x=0,
            y=6
        )
        
        self.skill_tile = construct_skill_tile()

        self.main_group.append(self.score_label)

    def create_bonus(self, x, y):
        if self.bonus:
            return
        skilllist = ["life", "skill"]
        bonus = Bonus(
            x=x,
            y=y,
            btype=skilllist[random.randint(0, 1)]
        )
        self.bonus = bonus
        self.main_group.append(self.bonus.sprite)

    def remove_bonus(self):
        if self.bonus:
            self.main_group.remove(self.bonus.sprite)
            self.bonus = None

    def update_bonus(self):
        if self.bonus:
            self.bonus.move(self.PIPE_SPEED)

            if self.bonus.eaten_by(self.bird):
                if self.bonus.btype == "life":
                    self.life = min(3, self.life + 1)
                elif self.bonus.btype == "skill":
                    self.skill = 1
                self.remove_bonus()

            elif self.bonus.is_off_screen():
                self.remove_bonus()

    def create_pipe(self, width):
        gap_y = random.randint(1, 63 - self.PIPE_GAP)

        pipe = Pipe(
            x=128,
            gap_y=gap_y,
            gap_h=self.PIPE_GAP,
            screen_h=64,
            palette=self.pipe_palette,
            width=width   
        )

        self.pipes.append(pipe)
        self.main_group.append(pipe.top)
        self.main_group.append(pipe.bottom)

        return 128 + width//2, gap_y + self.PIPE_GAP // 2
        
    def receive(self, cmd):
        if cmd == "kill":
            self.killed = True
            return
        if self.idle_frame_counter != 0:
            return
        if not self.skill_status:
            if cmd == "ACC":
                self.bird.jump(3)
                return
            if cmd == "bt2" and self.skill == 1:
                self.activate_skill()
        else:
            if cmd == "bt0":
                self.bird.jump(3)
            if cmd == "bt1":
                self.bird.jump(-3)

    def idle_for(self, frames):
        self.idle_frame_counter += frames

    def respawn(self):
        self.idle_for(60)
        self.anime_status = "respawn"
        self.bird.lock_to_spawn()
        self.main_group.remove(self.bird.sprite)
        self.main_group.append(self.bird.vis_2)

    def activate_skill(self):
        self.idle_for(100)
        self.anime_status = "activate_skill"
        self.skill_status = True
        self.bird.gravity = 0
        self.bird.vy = 0
        self.skill -= 1
        self.skill_timer = 333
        
    def stop_skill(self):
        self.idle_for(100)
        self.anime_status = "stop_skill"
        self.skill_status = False
        self.bird.gravity = 0.6

    def animating(self):
        if self.anime_status == "respawn":
            idle_frame = 60 - self.idle_frame_counter
            if idle_frame % 3 == 0:
                for pipe in self.pipes:
                    pipe.move(1)
                if self.bonus:
                    self.bonus.move(1)
            if idle_frame == 50:
                self.main_group.remove(self.bird.vis_2)
                self.main_group.append(self.bird.sprite)
        elif self.anime_status == "activate_skill":
            idle_frame = 100 - self.idle_frame_counter
            if idle_frame == 10 or idle_frame == 50 or idle_frame == 90:
                self.main_group.insert(0, self.skill_tile)
            if idle_frame == 30 or idle_frame == 70:
                self.main_group.remove(self.skill_tile)
        elif self.anime_status == "stop_skill":
            idle_frame = 100 - self.idle_frame_counter
            if idle_frame == 10 or idle_frame == 50 or idle_frame == 90:
                self.main_group.remove(self.skill_tile)
            if idle_frame == 30 or idle_frame == 70:
                self.main_group.insert(0, self.skill_tile)

    def update(self):
        if self.killed:
            return 
        if self.gameover or self.finished:
            return
        
        # ----- in idle ----
        if self.idle_frame_counter != 0:
            self.animating()
            self.idle_frame_counter -= 1
            return

        # ----- not in idle ----
        self.bird.update(64)
        if self.skill_status:
            self.bird.jump(0)
            if self.skill_timer == 0:
                self.stop_skill()
                return
            else:
                self.skill_timer -= 1

        self.frame += 1
        self.frame %= 40
        if self.frame == 0:
            if not self.finish_line:
                xp, yp = self.create_pipe(self.PIPE_WIDTH)
                if random.randint(1, 10) <= self.bonus_thresh:
                    self.create_bonus(xp, yp)
            if self.mode != "Infinite":
                self.progress += 1
                if self.progress == self.progress_step + self.last_progress_mark:
                    self.last_progress_mark += self.progress_step
                    self.PIPE_GAP -= 2  
        
        elif self.frame == 20:
            #print(self.progress, self.last_progress_mark)
            if not self.mode == "infinite" and self.progress == self.target_pipes :
                self.finish_line = FinishLine(x=128)
                self.main_group.append(self.finish_line.sprite)

        # ---- update ----
        self.update_bonus()
        
        new_pipes = []
        for idx, pipe in enumerate(self.pipes):
            pipe.move(self.PIPE_SPEED)

            if pipe.collides_with(self.bird):
                self.life -= 1

                if self.life > 0:
                    self.respawn()
                    return
                else:
                    self.gameover = True
                    return

            if pipe.passed_by(self.bird):
                self.score += 1
                self.score_label.text = f"Score: {self.score}"

            if idx == 0 and pipe.is_off_screen():
                self.main_group.remove(pipe.top)
                self.main_group.remove(pipe.bottom)
                pipe.top = None
                pipe.bottom = None
            else:
                new_pipes.append(pipe)

        self.pipes = new_pipes

        if self.finish_line:
            self.finish_line.move(self.PIPE_SPEED)

            if self.finish_line.collides_with(self.bird):
                self.finished = True
                self.finish_line = None
        
        return self.life, self.skill
