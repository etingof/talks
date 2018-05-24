import machine
import uasyncio as asyncio

led = machine.Pin(2, machine.Pin.OUT)

async def toggle(period):
    while True:
        await asyncio.sleep(period)
        if led.value():
            led.off()
        else:
            led.on()

loop = asyncio.get_event_loop()
for x in range(1, 3):
    loop.create_task(toggle(x))
loop.run_until_complete(asyncio.sleep(30))
loop.close()
