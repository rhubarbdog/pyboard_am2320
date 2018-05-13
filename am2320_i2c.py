# this code is based on
"""
https://github.com/mcauser/microbit-am2320

"""
# pyboard MicroPython for micro:bit Aosong AM2320 I2C driver
#
# modifications by Phil Hall


import ustruct
import time

class DataError(Exception):
    pass

class AM2320:
    def __init__(self, i2c=None, address=0x5c):
        self.__i2c = i2c
        self.__address = address

    def readSensor(self):
        # wake sensor
        try:
            self.__i2c.send(b'',self.__address)
        except OSError:
            pass

        # wait atleast 0.8ms but no more than 3ms
        time.sleep_ms(1)
        # read 4 registers starting at offset 0x00
        self.__i2c.send(b'\x03\x00\x04',self.__address)
        # wait at least 1.5ms
        time.sleep_ms(2)
        # read data
        buf = self.__i2c.recv(8,self.__address)

        # validate the first 2 bytes returned
        if buf[0]!=0x03 or buf[1]!=0x04:
            raise DataError("Invalid initial bytes.")
        
        crc = ustruct.unpack('<H', bytearray(buf[-2:]))[0]

        if (crc != self._crc16(buf[:-2])):
            raise DataError("Checksum error.")

        humid=(buf[2] << 8 | buf[3]) * 0.1
        temp = ((buf[4] & 0x7f) << 8 | buf[5]) * 0.1
        if buf[4] & 0x80:
            temp = -temp
        return (temp,humid)

    def _crc16(self, buf):
        crc = 0xFFFF
        for c in buf:
            crc ^= c
            for i in range(8):
                if crc & 0x01:
                    crc >>= 1
                    crc ^= 0xA001
                else:
                    crc >>= 1
        return crc
