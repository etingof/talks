import pyb

water = pyb.Pin('X2', pyb.Pin.IN, pyb.Pin.PULL_UP)
red_led = pyb.LED(1)
green_led = pyb.LED(2)

while True:
        print(water.value())
	if water.value():
		red_led.on()
		green_led.off()
	else:
		red_led.off()
		green_led.on()
