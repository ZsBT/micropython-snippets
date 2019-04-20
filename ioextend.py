"""
    IO extender for this chip
    """

class pcf8575:
    _bytes = [0,0]
    
    def __init__(self, i2c, addr=0x20):
        self.addr = addr
        self.i2c = i2c    

    # voltage high on pins (list)
    def on(self, pins):
        print("pcf8575 #ON#",pins)
        self.read()
        for pin in pins:
            self._bytes[0 if pin<8 else 1] |= 2**(pin % 8)
        return self._writeData()

    # voltage low on pins (list)
    def off(self, pins):
        print("pcf8575 #OFF#",pins)
        self.read()
        for pin in pins:
            self._bytes[0 if pin<8 else 1] &= 255-2**(pin % 8)
        return self._writeData()

    # return the 2 bytes read from IC
    def read(self):
        self._bytes = list(self.i2c.readfrom(self.addr,2))
        sleep_ms(20)
        return self._bytes
    
    # return bits as list
    def pins(self):
        (b1,b2) = self.read()
        lst = []
        for i in range(0,8):
            lst.append(b1 & 1)
            b1 >>= 1
        for i in range(0,8):
            lst.append(b2 & 1)
            b2 >>= 1
        return lst
        
    # write 2 bytes to IC
    def _writeData(self):
        wrtn = self.i2c.writeto(self.addr, bytes(self._bytes))
        sleep_ms(20)
        return wrtn
    
