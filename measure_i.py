import time
import os
import datetime
#from datetime import date
#from datetime import datetime
import datetime as dt
import ST7735
from PIL import Image, ImageDraw, ImageFont

try:
    # Transitional fix for breaking change in LTR559
    from ltr559 import LTR559
    ltr559 = LTR559()
except ImportError:
    import ltr559

from bme280 import BME280

from enviroplus import gas

from pms5003 import PMS5003, ReadTimeoutError

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import csv

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus
bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)
pms5003 = PMS5003()
import logging

logging.basicConfig(
    format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

# print to the user how to stop the program
logging.info("""We are now recording data from all the Enviro+ sensors.

Press Ctrl+C to exit!

""")

# Create LCD class instance.
disp = ST7735.ST7735(
    port=0,
    cs=1,
    dc=9,
    backlight=12,
    rotation=270,
    spi_speed_hz=10000000
)

# Initialize display.
disp.begin()

# Width and height to calculate text position.
WIDTH = disp.width
HEIGHT = disp.height

# New canvas to draw on.
img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))
draw = ImageDraw.Draw(img)

# Text settings.
font_size = 20
font = ImageFont.truetype("fonts/Asap/Asap-Bold.ttf", font_size)
text_colour = (255, 255, 255)
back_colour = (0, 170, 170)

message = "Stay back...\n collecting data"
size_x, size_y = draw.textsize(message, font)

# Calculate text position
x = (WIDTH - size_x) / 2
y = (HEIGHT / 2) - (size_y / 2)

# Draw background rectangle and write text.
draw.rectangle((0, 0, 160, 80), back_colour)
draw.text((x, y), message, font=font, fill=text_colour)
disp.display(img)

#initialise file to write data to
t = dt.datetime.now()
t = str(t)[:-7]
f = open("data/enviroData_" + t + ".txt","w+")

try:
    while True:
        pass
        a=dt.datetime.now()
        light = ltr559.get_lux()

        temperature = bme280.get_temperature()
        pressure = bme280.get_pressure()
        humidity = bme280.get_humidity()

        readings = gas.read_all()
        carbmon = readings.reducing
        nitrox = readings.oxidising
        ammonia = readings.nh3

#        pmreadings = PMS5003.read()
#        try:
#            pmreadings = pms5003.read()
#        except ReadTimeoutError:
#            pms5003 = PMS5003()

        try:
            pmreadings = pms5003.read()
        except ReadTimeoutError:
            pms5003 = PMS5003()
            pmreadings = pms5003.read()

        smallpm = pmreadings.pm_ug_per_m3(1.0)
        mediumpm = pmreadings.pm_ug_per_m3(2.5)
        largepm = pmreadings.pm_ug_per_m3(10)

        f.write( str(a) + "\t" + str(light) + "\t" + str(temperature) + "\t" + str(pressure) + "\t" + str(humidity) + "\t" + str(carbmon) + "\t" + str(nitrox) + "\t" + str(ammonia) + "\t" + str(smallpm) + "\t" + str(mediumpm) + "\t" + str(largepm) + "\n")
        time.sleep(30)

except KeyboardInterrupt:
    disp.set_backlight(0)
    pass
finally:
    f.close()
