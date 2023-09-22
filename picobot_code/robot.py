"""
MicroPython code for Pico car project using:
* Raspberry Pi Pico mounted on differential drive car
* 56:1 gear motors with encoders
"""

from machine import Pin, PWM
from parameters import FULL_SPD, LOW_SPD


# setup pins connected to L298N Motor Drive Controller Board
ena = PWM(Pin(21))
in1 = Pin(20, Pin.OUT, value=0)
in2 = Pin(19, Pin.OUT, value=0)
in3 = Pin(18, Pin.OUT, value=0)
in4 = Pin(17, Pin.OUT, value=0)
enb = PWM(Pin(16))

ena.freq(1_000)
enb.freq(1_000)

class Robot():

    def __init__(self):
        self.spd = 0.7

    def faster(self):
        print("faster")
        if self.spd <= 0.9:
            self.spd += 0.1

    def slower(self):
        print("slower")
        if self.spd >= 0.2:
            self.spd -= 0.1

    def forward(self):
        print("forward")
        set_mtr_dirs('FWD', 'FWD')
        set_mtr_spd(self.spd)

    def backward(self):
        print("backward")
        set_mtr_dirs('REV', 'REV')
        set_mtr_spd(self.spd)

    def left(self):
        print("left")
        set_mtr_dirs('REV', 'FWD')
        set_mtr_spd(self.spd/2)

    def right(self):
        print("right")
        set_mtr_dirs('FWD', 'REV')
        set_mtr_spd(self.spd/2)

    def stop(self):
        print("stop")
        set_mtr_dirs('OFF', 'OFF')
        set_mtr_spd(0)


def set_mtr_dirs(a_mode, b_mode):
    """Set motor direction pins for both motors.
    options are: 'FWD', 'REV', 'OFF'."""

    if a_mode == 'FWD':
        in1.value(0)
        in2.value(1)
    elif a_mode == 'REV':
        in1.value(1)
        in2.value(0)
    else:  # Stopped
        in1.value(0)
        in2.value(0)

    if b_mode == 'FWD':
        in3.value(0)
        in4.value(1)
    elif b_mode == 'REV':
        in3.value(1)
        in4.value(0)
    else:  # Stopped
        in3.value(0)
        in4.value(0)

def set_mtr_spd(spd):
    """0 < spd < 1"""
    pwm_spd = int(FULL_SPD * spd)
    if pwm_spd < LOW_SPD:
        pwm_spd = LOW_SPD
    ena.duty_u16(pwm_spd)
    enb.duty_u16(pwm_spd)


