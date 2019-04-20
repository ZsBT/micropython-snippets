#
# https://github.com/ZsBT/micropython-snippets
# 
#	temperature/humidity sensor classes for ESP8266/ESP32 boards, for MicroPython system.
#	DHT is supported off-the-shelf so no need to program it.
#

import time


# LM75 temp/humidity sensor, I2C interface
class LM75:
	# Constructor. Pass a machine.I2C instance where the device is connected
	def __init__(self,i2c):
		self.i2c = i2c
	
	# read temperature, returns float
	def readTemp(self, addr=0x48):
		value = self.i2c.readfrom(addr, 2)
		return float(value[0]+value[1]/100)


# HTU21D temperature/humidity sensor, I2C interface
# based on the work of https://github.com/manitou48/pyboard - respect mate.
class HTU21D:
	i2c = None
	lastTemp = None
	lastRH = None
  
	# HTU21D Address
	address = 0x40
	

	# Constructor. Pass a machine.I2C instance where the device is connected
	def __init__(self,i2c):
		self.i2c = i2c
	
	# read temperature
	def readTemp(self):
		self.reset()
		
		# temperature command, HOLD bus
		self.i2c.writeto(self.address, b'\xe3')
		
		# wait measurement
	        time.sleep(.05)

		#Read 3 temperature bytes from the sensor
		# value[0], value[1]: Raw temperature data
		# value[2]: CRC
		value = self.i2c.readfrom(self.address,3)
		
		if not self.crc8check(value):
			return -255
			
		rawTempData = ( value[0] << 8 ) + value[1]
		
		rawTempData = rawTempData & 0xFFFC; # Clear the status bits
		
		# Calculate the actual temperature
		actualTemp = -46.85 + (175.72 * rawTempData / 65536)
		self.lastTemp = actualTemp
		
		return actualTemp

	# read relative humidity
	def readRH(self):
		self.reset()
		
		# humidity command, HOLD bus
		self.i2c.writeto(self.address, b'\xe5')
		
		# read measurement
	        time.sleep(.05)
	        
		#Read 3 humidity bytes from the sensor
		# value[0], value[1]: Raw relative humidity data
		# value[2]: CRC
		value = self.i2c.readfrom(self.address,3)
		
		if not self.crc8check(value):
			return False

		rawRHData = ( value[0] << 8 ) + value[1]
		
		rawRHData = rawRHData & 0xFFFC; # Clear the status bits
		
		# Calculate the actual RH
		actualRH = -6 + (125.0 * rawRHData / 65536)
		self.lastRH = actualRH
		
		return actualRH
	
	def crc8check(self, value):
		#Calulate the CRC8 for the data received
		# from https://github.com/sparkfun/HTU21D_Breakout
		remainder = ( ( value[0] << 8 ) + value[1] ) << 8
		remainder |= value[2]
		
		# POLYNOMIAL = 0x0131 = x^8 + x^5 + x^4 + 1
		# divsor = 0x988000 is polynomial shifted to farthest left of three bytes
		divsor = 0x988000
		
		for i in range(0, 16):
			if( remainder & 1 << (23 - i) ):
				remainder ^= divsor

			divsor = divsor >> 1
		
		if remainder == 0:
			return True
		else:
			return False

	def reset(self):
		self.i2c.writeto(self.address, b'\xfe')
		time.sleep(.02)
	
