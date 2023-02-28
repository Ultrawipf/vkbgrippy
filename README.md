# vkbgrippy
Gamepad interface for VKB SCG grips using circuitpython.

Still in development and may not work correctly.



Written for RP2040 devboards and requires the usb_hid library.

You can uncomment the neopixel feedback if your board has no LED.


### Connections:
Red wire to 3.3v, black to GND and center yellow to GPIO 2 (UART RX) and a 5k resistor between GPIO1 (UART TX) and GPIO2 (UART RX).