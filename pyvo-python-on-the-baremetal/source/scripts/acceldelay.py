import pyb

led = pyb.LED(3)

acc = pyb.Accel()

def remap(i_val, i_start, i_stop, o_start, o_stop):
	o_val =  o_start + (o_stop - o_start) * ((i_val - i_start)/(i_stop - i_start))
	return o_val
	
while True:
	intensity = int(remap(acc.x(), -30, 30, 10, 1000))
        print(intensity)
	led.toggle()
	pyb.delay(intensity)
