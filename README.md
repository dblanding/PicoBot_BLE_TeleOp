# TeleOperated PicoBot using Bluetooth (BLE) communication between two Pico-W devices

* Implementation of Kevin McAleer's [Bluetooth remote controlled robot tutorial](https://www.kevsrobots.com/blog/bluetooth-remote.html) but with the following variations:
    * For the remote control, I will use a [Pico LCD 1.14](https://www.waveshare.com/wiki/Pico-LCD-1.14) device instead of the Pimoroni Display device used by Kevin
    * The robot is my own PicoBot instead of Kevin's BurgerBot
* Kevin's tutorial does an excellent job of explaining all the important details, so I won't attempt to repeat them here.
* There is just one small edit I made in the next to last line of `peripheral_task` of the remote (server) code.
    * `await connection.disconnected(timeout_ms=None)`
    * Without this, the timeout value defaults to 60 seconds, disconnecting the client after 1 minute.

## The [Remote](https://www.waveshare.com/wiki/Pico-LCD-1.14) Control:
![Pico LCD 1.14 Display](imgs/lcd_remote.jpg)

## The [PicoBot](https://github.com/dblanding/Pico-MicroPython-smart-car):
![PicoBot](imgs/picobot.png)

## To operate:
1. Power-up the Remote. (This is the BLE server.)
2. Turn on the PicoBot. (This is the BLE client.)
3. Use **A** button to increase speed, **B** button to decrease speed.
4. Use joystick control to control PicoBot movement.

![joystick control](imgs/5-button_form.png)

