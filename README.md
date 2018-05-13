# pyboard_am2320
an i2c driver for the pyboard and AOSONG am2320 temperature and humidity sensor.

The example connects the sensor to I2C 2 pins Y9 and Y10.
The sensor has 4 pins from the front (grill forwards) left to right they are :
pin 1 - Vcc (3.3v). 
pin 2 - SDA. 
pin 3 - Ground. 
pin 4 - SCL. 

The pyboard has pull up resistors built in, conforming to the I2C specification, if the sensor is on a long wire you may need to add external pull up resistors

