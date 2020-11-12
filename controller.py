import time
import multiprocessing
from rpi_ws281x import PixelStrip, Color
import sys


functions = {} # key is the keyword and the value is the function to call when that keyword is entered


LED_COUNT = 300        # Number of LED pixels.
LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10    # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 125 # Set to 0 for darkest and 255 for brightest
LED_INVERT = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

def init_cmd_keywords():
    def add_function(keyword, func, help_msg):
        functions[keyword] = {}
        functions[keyword]['action'] = func
        functions[keyword]['help'] = help_msg

    # initialize commands    
    add_function('on', turn_on, 'turns on the led strip.')
    add_function('off', turn_off, 'turns off the led strip.')
    
def turn_on(strip):
    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color(150,0,150))
    strip.show()
    time.sleep(1000000)

def turn_off(strip):
    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color(0,0,0))
    strip.show()
    time.sleep(1000000)

def parse_input(keyword):
    for expected_keyword in functions:
        if expected_keyword == keyword.lower().strip():
            return functions[expected_keyword]['action']
        print("%s is not %s" % (expected_keyword, keyword.lower()))
    return None

def help():
    global functions
    print("Usage:")
    for keyword in functions:
        print("%s: %s" % (keyword, functions[keyword]['help']))

if __name__ == '__main__':
    print("Welcome to the LED Animation Studio! ")
    print("")
    init_cmd_keywords()
    leds = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    leds.begin()
    process = None
    try:
        while True:
            cmd = raw_input("> ")
            print(cmd)
            action = parse_input(cmd)
            if action == None:
                help()
                continue
            elif process != None:
                process.terminate()
            process = multiprocessing.Process(target=action, args=(leds,))
            process.start()
    except KeyboardInterrupt:
        turn_off(leds)
        sys.exit(0)

