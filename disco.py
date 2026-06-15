import board
import busio
import digitalio
import random
import time
from adafruit_neotrellis.neotrellis import NeoTrellis
from rainbowio import colorwheel


# some color definitions
OFF = (0, 0, 0)


# Create the I2C object for the trellis
i2c_bus = busio.I2C(board.SCL, board.SDA)
print(f"{i2c_bus.scan()=}")

# Create the trellis
trellis = NeoTrellis(i2c_bus, addr=0x2E)

# Turn off all LEDs
for i in range(16):
    trellis.pixels[i] = OFF

while True:
    for i in range(16):
        trellis.pixels[i] = colorwheel(random.randrange(256))

