# Hello World Example
#
# Welcome to the OpenMV IDE! Click on the green run arrow button below to run the script!

import sensor, image, time,pyb
from pyb import LED
from pyb import Pin
p0_pin = pyb.Pin.board.P0
p0_pin.init(Pin.IN,Pin.PULL_UP)
def led_blink(x):
    led = pyb.LED(x)
    led.on()
    time.sleep(5)
    led.off()
sensor.reset()                      # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)   # Set frame size to QVGA (320x240)
#sensor.skip_frames(time = 2000)     # Wait for settings take effect.
sensor.skip_frames(5)
clock = time.clock()                # Create a clock object to track the FPS.

while(True):
    if p0_pin.value():
        sensor.set_pixformat(sensor.GRAYSCALE)
        led_blink(3)
    else:
        sensor.set_pixformat(sensor.RGB565)
        led_blink(2)
    clock.tick()                    # Update the FPS clock.
    img = sensor.snapshot()         # Take a picture and return the image.
    print(clock.fps())              # Note: OpenMV Cam runs about half as fast when connected
                                    # to the IDE. The FPS should increase once disconnected.
