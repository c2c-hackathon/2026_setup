import board
import busio
import digitalio
import time
from adafruit_neotrellis.neotrellis import NeoTrellis

# Setup interrupt (INT) pin
int_pin = digitalio.DigitalInOut(board.D4)
int_pin.direction = digitalio.Direction.INPUT
print(f"{int_pin.value=}")

#create the i2c object for the trellis
i2c_bus = busio.I2C(board.SCL, board.SDA)
print(f"{i2c_bus.scan()=}")

#create the trellis
# trellis = NeoTrellis(i2c_bus, addr=0x2E)
