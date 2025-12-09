import time
import pwmio

class Buzzer:
    def __init__(self, pin):
        self.buzzer = pwmio.PWMOut(
            pin,
            duty_cycle=0,
            frequency=1000,
            variable_frequency=True
        )

    def tone(self, freq, duration):
        self.buzzer.frequency = freq
        self.buzzer.duty_cycle = 32768  
        time.sleep(duration)
        self.buzzer.duty_cycle = 0
        time.sleep(0.05)

    def stop(self):
        self.buzzer.duty_cycle = 0

    def victory_sound(self):
        melody = [
            (523, 0.12),   # C5
            (659, 0.12),   # E5
            (784, 0.12),   # G5
            (1046, 0.25),  # C6
            (784, 0.12),   # G5
            (1046, 0.35),  # C6
        ]
        for freq, dur in melody:
            self.tone(freq, dur)

    def fail_sound(self):
        melody = [
            (784, 0.15),   # G5
            (659, 0.15),   # E5
            (523, 0.2),    # C5
            (392, 0.4),    # G4
        ]
        for freq, dur in melody:
            self.tone(freq, dur)

    def startup_sound(self):
        melody = [
            (196, 0.12),   # G3
            (262, 0.12),   # C4
            (330, 0.12),   # E4
            (392, 0.12),   # G4
            (523, 0.25),   # C5
        ]
        for freq, dur in melody:
            self.tone(freq, dur)

    def deinit(self):
        self.buzzer.deinit()
