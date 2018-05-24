import pyb

leds = [pyb.LED(n) for n in range(1,5)]
acc = pyb.Accel()

x = 0
led = 1

while True:
    leds[led].off()
    acc_reading = acc.x()
    x += acc_reading
    if x < 0:
        x += 799
    elif x > 799:
        x -= 799
    led = x // 200
    leds[led].on()
    pyb.delay(5)
