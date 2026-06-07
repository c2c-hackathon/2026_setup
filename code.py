import board
import busio
import digitalio
import time
from adafruit_neotrellis.neotrellis import NeoTrellis

#create the i2c object for the trellis
i2c_bus = busio.I2C(board.SCL, board.SDA)

#create the trellis
# trellis = NeoTrellis(i2c_bus, addr=0x2E)
