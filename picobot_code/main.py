# Adapted from KevsRobot.com

import aioble
import bluetooth
import machine
import uasyncio as asyncio
from robot import Robot

# Bluetooth UUIDS can be found online at https://www.bluetooth.com/specifications/gatt/services/

_REMOTE_UUID = bluetooth.UUID(0x1848)
_GENERIC_UUID = bluetooth.UUID(0x1848) 
_REMOTE_CHARACTERISTICS_UUID = bluetooth.UUID(0x2A6E)

led = machine.Pin("LED", machine.Pin.OUT)
connected = False
alive = False

bot = Robot()
bot.stop()


async def find_remote():
    # Scan for 5 seconds, in active mode, with very low interval/window (to
    # maximise detection rate).
    async with aioble.scan(5000, interval_us=30000, window_us=30000, active=True) as scanner:
        async for result in scanner:

            # See if it matches our name
            if result.name() == "KevsRobots":
                print("Found KevsRobots")
                for item in result.services():
                    print (item)
                if _GENERIC_UUID in result.services():
                    print("Found Robot Remote Service")
                    return result.device
            
    return None


async def blink_task():
    """ Blink the LED on and off every second """
    
    print('blink task started')
    toggle = True
    
    while True and alive:
        blink = 250
        led.value(toggle)
        toggle = not toggle
        # print(f'blink {toggle}, connected: {connected}')
        if connected:
            blink = 1000
        else:
            blink = 250
        await asyncio.sleep_ms(blink)
    print('blink task stopped')


def move_robot(command):
    if command == b'a':
        print("A button pressed")
        bot.faster()

    elif command == b'b':
        print("B button pressed")
        bot.slower()

    elif command == b'u':
        print("UP button pressed")
        bot.forward()

    elif command == b'd':
        print("DOWN button pressed")
        bot.backward()

    elif command == b'r':
        print("RIGHT button pressed")
        bot.right()

    elif command == b'l':
        print("LEFT button pressed")
        bot.left()

    elif command == b'c':
        print("CNTR button pressed")
        bot.stop()


async def peripheral_task():
    print('starting peripheral task')
    global connected, alive
    connected = False
    device = await find_remote()
    if not device:
        print("Robot Remote not found")
        return
    try:
        print("Connecting to", device)
        connection = await device.connect()
        
    except asyncio.TimeoutError:
        print("Timeout during connection")
        return
      
    async with connection:
        print("Connected")
        alive = True
        connected = True

        robot_service = await connection.service(_REMOTE_UUID)
        control_characteristic = await robot_service.characteristic(_REMOTE_CHARACTERISTICS_UUID)
        
        while True:
            try:
                if robot_service == None:
                    print('remote disconnected')
                    alive = False
                    break
                
            except asyncio.TimeoutError:
                print("Timeout discovering services/characteristics")
                alive = False
                break
            
            if control_characteristic == None:
                print('no control')
                alive = False
                break
           
            try:
                data = await control_characteristic.read(timeout_ms=1000)

                await control_characteristic.subscribe(notify=True)
                while True:
                    command = await control_characteristic.notified()
                    move_robot(command)
                                                                                
            except Exception as e:
                print(f'something went wrong; {e}')
                connected = False
                alive = False
                break
        await connection.disconnected()
        print(f'disconnected')
        alive = False
                
async def main():
    tasks = []
    tasks = [
        asyncio.create_task(blink_task()),
        asyncio.create_task(peripheral_task()),
    ]
    await asyncio.gather(*tasks)
    
while True:
    asyncio.run(main())
