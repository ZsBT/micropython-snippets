"""
    class for Micro Servo 9g motor, model SG90
    
    tested under ESP8266, where the max PWM duty is 512.
    
    @author github.com/ZsBT
"""
from machine import Pin,PWM

class SG90:
    Hz = 50
    DutyMin = 25
    DutyMax = 128
    DutyAngle = 180
    
    def __init__(self, pin):
        self.pwm = PWM(Pin(pin), freq=SG90.Hz, duty=0)
        self.m = (SG90.DutyMax-SG90.DutyMin)/SG90.DutyAngle
        
    def move(self,angle):
        if 0 < angle < SG90.DutyAngle:
            self.pwm.duty(int(angle*self.m)+self.DutyMin)
        
    def __deinit__(self):
        self.pwm.deinit()
    
