import time
import board
from buzzer_class import Buzzer

buzzer = Buzzer(board.D10)

while True:
    print("Victory Sound!")
    buzzer.victory_sound()

    time.sleep(2)

    print("Fail Sound!")
    buzzer.fail_sound()

    time.sleep(2)
    
    print("start sound")
    buzzer.startup_sound()
    
    time.sleep(2)
