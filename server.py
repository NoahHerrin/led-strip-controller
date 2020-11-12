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
import random
from rpi_ws281x import PixelStrip, Color

# Animation Constants
ACTIVE= Color(0,0,0)
NEW_REQUEST = False
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
    # initialize socket, and set it to listen.
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", PORT))
    server.listen(5)
    
    while True:
        print('Waiting connections.')
        client, address = server.accept()
        msg = ''
        while msg != 'end':
            data = client.recv(1024)
            if data != None:
                msg = data.decode('ascii').lower()
                if msg == 'color':
                    client.send(random.choice(['red', 'blue', 'green']))
                elif msg == 'number':
                    client.send(str(random.randint(1,10)))
                else:
                    client.send('I do not understand.')
        client.close()
def update_animation():
    change_animation
    call_animation(args)
def animation1():
    while not NEW_REQUEST:
        # animate
    
if __name__ == '__main__':
    server()

