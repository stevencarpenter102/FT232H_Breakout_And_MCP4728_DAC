"""
set-up steps! (see here: https://learn.adafruit.com/circuitpython-on-any-computer-with-ft232h)
distilled instructions below, based on link above + TCA9548a instructions:
     1) installed blinka via pip (pip3 install Adafruit-Blinka)
     2) install zadig (https://learn.adafruit.com/circuitpython-on-any-computer-with-ft232h/windows) and setup FT232H w/ libusbK driver
     3) turn "i2c mode on" physically on the FT232H board
     4) install adafruit's mcp4728 library (pip3 install adafruit-circuitpython-mcp4728_0)
     5) pip3 install adafruit-circuitpython-tca9548a
"""
import os

# not sure if this should be here...or needs to be done command line?
os.environ['BLINKA_FT232H'] = '1'  # Enable FT232H

import usb
import usb.util
import board
import adafruit_mcp4728
import adafruit_tca9548a
import digitalio
import time
import mcp42728_read_write_i2caddress
from ACB_pin_mapping_base import ACBPinMap

# troubleshooting stuff here :-)
# print(dir(board))
# expect a printout for lines below!
# dev = usb.core.find(idVendor=0x0403, idProduct=0x6014)
# print(dev)

i2c = board.I2C()   # uses board.SCL and board.SDA
tca = adafruit_tca9548a.TCA9548A(i2c)

# OAHU-specific mapping
# write_analog(HEATER_TEMP1, float(value))

# swtich (HEATER_TEMP1 = SPIO_CS0_IN4)
#     get_dac(SPI0_CS_In4) = returns 

# mcp4728_0_A1 = adafruit_mcp4728.MCP4728(tca[0], 0x60 + )
# # mcp4728_0 = adafruit_mcp4728.MCP4728(i2c, 0x61)

def int_mcp4728_devices()

mcp4728_0.channel_a.value = int(65535/2) # Voltage = VDD
mcp4728_0.channel_b.value = int(65535/2) # VDD/2
mcp4728_0.channel_c.value = int(65535/4) # VDD/4
mcp4728_0.channel_d.value = 0 # 0V

# ldac_pin = digitalio.DigitalInOut(board.C0)
# ldac_pin.direction = digitalio.Direction.OUTPUT

# read_i2c_address(board.C0)

# while True:
#     ldac_pin.value = True
#     time.sleep(0.5)
#     ldac_pin.value = False
#     time.sleep(0.5)
