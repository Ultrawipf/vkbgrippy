import usb_hid
# from hid_gamepad import Gamepad
from time import sleep
import board
import neopixel
import busio
import grips
 
# led GP25, ws2812 gp23
ledw = neopixel.NeoPixel(board.GP23,1,auto_write=True)
ledw.brightness = 0.1
def setRgb(r,g,b):
    ledw[0] = [r,g,b]

uart = busio.UART(board.GP0, board.GP1, baudrate=500000,timeout = 0.25)
grip = grips.Kosmosima(uart,usb_hid.devices,10)


# Starts at button 1
while 1:
    sleep(0.075)
    
    if(grip.request()):
        setRgb(0,255,0)
        grip.send_report()
    else:
        setRgb(255,0,0)
