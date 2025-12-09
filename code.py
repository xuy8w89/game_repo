import time, random
import board, busio, displayio
import i2cdisplaybus, adafruit_displayio_ssd1306
import adafruit_adxl34x
import digitalio

from rankings import Rankings
from new_high_score_page import NewHighScorePage
from startup_animation import StartupAnimation
from buzzer_class import Buzzer
from gameloop import gameloop
from option_page import OptionPage
from game_over import GameOverPage
from finish_page import FinishPage
from rotary import Rotary
from led_class import FiveLEDs

# ===== 屏幕初始化 =====
displayio.release_displays()
i2c = busio.I2C(board.SCL, board.SDA)
display_bus = i2cdisplaybus.I2CDisplayBus(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)
main_group = displayio.Group()
display.root_group = main_group

# ===== IMU =====
accelerometer = adafruit_adxl34x.ADXL345(i2c)
last_acc = accelerometer.acceleration

# ===== 旋转编码器 =====
rotary = Rotary(board.D7, board.D8, board.D9)

button0 = digitalio.DigitalInOut(board.D0)
button1 = digitalio.DigitalInOut(board.D1)
button2 = digitalio.DigitalInOut(board.D2)
button0.direction = digitalio.Direction.INPUT
button0.pull = digitalio.Pull.UP   # ✅ 打开内部上拉
button1.direction = digitalio.Direction.INPUT
button1.pull = digitalio.Pull.UP   # ✅ 打开内部上拉
button2.direction = digitalio.Direction.INPUT
button2.pull = digitalio.Pull.UP   # ✅ 打开内部上拉

# ===== 页面管理 =====
status = "select_mode"


fiveled = FiveLEDs(board.D3)
buzzer = Buzzer(board.D10)
score = 0

# ===== 启动动画 =====
startup = StartupAnimation(main_group)
startup.play()
buzzer.startup_sound()

# ===== 动画结束后再显示 option_page =====
option_page = OptionPage(main_group)
game_manager = gameloop(main_group)
game_over_page = GameOverPage(main_group)
finish_page = FinishPage(main_group)
rankings_page = Rankings(main_group)
new_high_score_page = NewHighScorePage(main_group)

pending_score = 0

# ===== 主循环 =====
while True:
    direction, pressed = rotary.read()

    # -------- 选择界面 --------
    if status == "select_mode":
        if direction == 1:
            option_page.receive("DOWN")

        if not button2.value:
            option_page.clear_figure()
            rankings_page.show()
            status = "rankings"

        if pressed:
            option_page.receive("PRESS")

        result = option_page.get_result()
        if result:
            option_page.clear_figure()
            print(result)
            game_manager.init_game(result)   # 传入难度
            fiveled.reset()
            status = "gaming_level"

    # -------- 游戏中 --------
    elif status == "gaming_level":
        
        x, y, z = accelerometer.acceleration
        lx, ly, lz = last_acc
        diff = ((x-lx)**2 + (y-ly)**2 + (z-lz)**2) ** 0.5
        last_acc = (x, y, z)

        if direction == 1:
            game_manager.receive("kill")

        if diff > 6:
            game_manager.receive("ACC")
            
        if not button0.value:   # 按下 = False
            game_manager.receive("bt0")
            
        if not button1.value:   # 按下 = False
            game_manager.receive("bt1")
            
        if not button2.value:   # 按下 = False
            game_manager.receive("bt2")

        light_status = game_manager.update()
        if light_status:
            fiveled.set_lights(light_status)
        
        if game_manager.killed:
            game_manager.wrap_up()
            fiveled.reset()
            option_page.refresh()
            status = "select_mode"
        
        elif game_manager.gameover:
            score = game_manager.score
            game_manager.wrap_up()
            if game_manager.mode == "Infinite" and rankings_page.is_high_score(score):
                pending_score = score
                new_high_score_page.show()
                status = "new_record"
                buzzer.victory_sound()
            else:
                game_over_page.show(score)
                fiveled.reset()
                status = "game_over"
                buzzer.fail_sound()
            
        elif game_manager.finished:
            level = game_manager.mode
            game_manager.wrap_up()
            finish_page.show(level)
            fiveled.reset()
            status = "finished"
            buzzer.victory_sound()
            
    # -------- 结束界面1 --------
    elif status == "game_over":
        if pressed:
            game_over_page.receive("PRESS")

        if game_over_page.restart:
            status = "select_mode"
            game_over_page.clear_figure()
            option_page.refresh()
            
    elif status == "finished":
        if pressed:
            finish_page.receive("PRESS")
        
        if finish_page.restart:
            status = "select_mode"
            finish_page.clear_figure()
            option_page.refresh()
            
    elif status == "new_record":
        if direction == 1:
            new_high_score_page.receive("DOWN")

        if not button2.value:
            new_high_score_page.receive("PRESS")

        if new_high_score_page.done:
            rankings_page.insert(new_high_score_page.name, pending_score)
            new_high_score_page.clear_figure()
            rankings_page.show()
            status = "rankings"
            
    elif status == "rankings":
        if not button2.value:
            rankings_page.receive("PRESS")

        if pressed:       # ✅ 清空排行榜
            rankings_page.receive("CLEAR")

        if rankings_page.restart:
            rankings_page.clear_figure()
            option_page.refresh()
            status = "select_mode"

    
    time.sleep(0.03)
