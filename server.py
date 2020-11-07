"""
File: server.py
Author: Noah Herrin
Created: 11/7/2020

Purpose: two threaded script. one thread controls the animations on
the led strip. The other thread acts as a server, waiting for animation
requests from any client that connects. 

"""


import sys
import time
import math
import socket
import threading
from rpi_ws281x import PixelStrip, Color

# Animation Constants
ACTIVE= Color(0,0,0)
ENABLED = True
LED_COUNT = 300        # Number of LED pixels.
LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10    # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 125 # Set to 0 for darkest and 255 for brightest
LED_INVERT = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Networking Constants
SERVER_ADDRESS = '127.0.0.1'
PORT = 5003
QUEUE_LEN = 5

def server():
    global ACTIVE
    # initialize socket, and set it to listen.
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", PORT))
    server.listen(5)
    
    while True:
        print('Waiting connections.')
        client_socket, address = server.accept()
        data = client_socket.recv(1024)
        if data != None:
            msg = data.decode("ascii").lower()
            if msg == 'red':
                ACTIVE = Color(255,0,0)
            elif msg == 'blue':
                ACTIVE = Color(0,0,255)
            elif msg == 'green':
                ACTIVE = Color(0,255,0)
            else:
                print("unknown color.")
        client_socket.close()
        
def setup():
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()
    return strip

def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)

def update(strip, lights, color):
    for idx in range(0, len(lights) -1):
        strip.setPixelColor(idx, lights[idx])
    lights.pop(0)
    lights.append(color)

def led_engine():
    global ACTIVE
    strip = setup()
    leds = [Color(0,0,0) for i in range(LED_COUNT)]
    update(strip, leds, Color(0,0,0))
    strip.show()
    while ENABLED:
        print("hi")
        update(strip, leds, ACTIVE)
        strip.show()
    print('done')

if __name__ == '__main__':
    print("Hello, World!")
    engine = threading.Thread(target=server)
    engine.start()
    # engine.join()
    led_engine()
