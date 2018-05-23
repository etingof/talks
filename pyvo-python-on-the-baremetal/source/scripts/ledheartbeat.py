import pyb

led = pyb.LED(4)

tick = 0

while True:
    if tick <= 3:
        led.toggle()
    tick = (tick + 1) % 10
    pyb.delay(100)
