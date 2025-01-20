"""
set-up steps! (see here: https://learn.adafruit.com/circuitpython-on-any-computer-with-ft232h)
distilled instructions below, based on link above:
     1) installed blinka via pip (pip3 install Adafruit-Blinka)
     2) install zadig (https://learn.adafruit.com/circuitpython-on-any-computer-with-ft232h/windows) and setup FT232H's driver
     3) turn "i2c mode on" physically on the FT232H board
     4) install adafruit's mcp4728 library (pip3 install adafruit-circuitpython-mcp4728)

    Alternate:
    1) install FTDI D2XX drivers https://ftdichip.com/drivers/d2xx-drivers/
    2) 
"""
import os

# not sure if this should be here...or needs to be done command line?
# os.environ['BLINKA_FT232H'] = '1'  # Enable FT232H

# import usb
# import usb.util
# import board
import adafruit_mcp4728

from deprecated.ADC_ft232h_devices_ import FTD2XXI2C 

# troubleshooting stuff here :-)
# print(dir(board))
# expect a printout for lines below!
# dev = usb.core.find(idVendor=0x0403, idProduct=0x6014)
# print(dev)

# i2c = board.I2C()   # uses board.SCL and board.SDA
i2c = FTD2XXI2C()
buf = bytearray(4)
i2c.readfrom_into(0x60, buf)  # Replace 0x60 with your device's I2C address
print(buf)

# mcp4728 =  adafruit_mcp4728.MCP4728(i2c)

# mcp4728.channel_a.value = 65535 # Voltage = VDD
# mcp4728.channel_b.value = int(65535/2) # VDD/2
# mcp4728.channel_c.value = int(65535/4) # VDD/4
# mcp4728.channel_d.value = 0 # 0V