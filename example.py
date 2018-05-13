import pyb
import am2320_i2c as AOSONG

DELAY=350

# ERROR   all lights on

#         red flashing
TEMP_COLD=17
#         red
TEMP_COOL=19
#         green
TEMP_OK=21
#         amber
TEMP_HIGH=23
#         blue
TEMP_HOT=25
#         blue flashing

lights=[pyb.LED(1),pyb.LED(2),pyb.LED(3),pyb.LED(4)]

def all_lights_off(ignore=None):
    for i in range(4):
        if ignore!=None and i!=ignore:
            lights[i].off()


def main():

    i2c=pyb.I2C(2,pyb.I2C.MASTER,baudrate=100000)
    am2320=AOSONG.AM2320(i2c)
    
    while True:

        try:
            temp,_=am2320.readSensor()
        except:
            error=True
        else:
            error=False

                
        for loop in range(10):

            if error:
                for led in lights:
                    led.on()


            elif temp<TEMP_COLD:
                all_lights_off(0)
                lights[0].toggle()
                
            elif temp>=TEMP_COLD and temp<TEMP_COOL:
                all_lights_off(0)
                lights[0].on()

            elif temp>=TEMP_COOL and temp<TEMP_OK:
                all_lights_off(1)
                lights[1].on()

            elif temp>=TEMP_OK and temp<TEMP_HIGH:
                all_lights_off(2)
                lights[2].on()

            elif temp>=TEMP_HIGH and temp<TEMP_HOT:
                all_lights_off(3)
                lights[3].on()
        
            else:
                all_lights_off(3)
                lights[3].toggle()

            pyb.delay(DELAY)
 
if __name__=="__main__":
    main()
