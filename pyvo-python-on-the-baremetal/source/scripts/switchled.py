import pyb

sw = pyb.Switch()
led = pyb.LED(4)

while True:
    if sw() == True:
        led.on()
    else:
        led.off()
