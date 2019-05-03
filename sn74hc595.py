from machine import Pin,SPI
from utime import sleep_ms

"""
	send byte(s) to the famous 74hc595 shift register IC
	using the SPI interface
	@author github.com/ZsBT
	
	MCU-IC connections:
	MOSI -> SER/DS/pin14 (this is data line)
	SCLK -> SRCLK/SH_CP/pin11 (this is clock line)
	any GPIO pin -> RCLK/ST_CP/pin12 (this is the latch pin)
	
	IC connections:
	SRCRL/MR/pin10 to ground
	OE/pin13 to VCC
	optionally daisy-chain with connecting first IC pin9 to second IC pin14
"""	

class sn74hc595:

    # spibus is the MCU's HW interface
    # enablePin is any GPIO output pin
    # baud is the speed, max approx. 4MHz
    def __init__(self, spibus=1, enablePin=2, baud=4000000):
        self.latchPin = Pin(enablePin,Pin.OUT)
        self.latchPin.value(0)
        self.spi = SPI(spibus)
        self.spi.init(baud)
    
    # list of bytes to send. one byte per IC
    def write(self, listofbytes):
        self.latchPin.value(0)
        print("sending",listofbytes)
        self.spi.write( bytearray(listofbytes))
        self.latchPin.value(1)
    

    # example method: endless loop for two, daisy-chained IC-s
    def knightrider(self, slp=100):
        b=1
        while True:
            while not b & 0b1000000000000000:
                self.write( [ b>>8, b&0xff])
                b <<= 1
                sleep_ms(slp)
            while not b&1:
                self.write( [ b>>8, b&0xff])
                b >>= 1
                sleep_ms(slp)

S=sn74hc595()
S.knightrider(slp=50)

