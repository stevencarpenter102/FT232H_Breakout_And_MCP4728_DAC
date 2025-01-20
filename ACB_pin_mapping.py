"""
The ACB has ADC pins (from ADC128S102 chips on-board) exposed to the outside world.
To control the voltages on these pins, MCP4728 DAC's have been connected to each channel's input.
This files contains the mapping for 'ADC pins'---->'DAC's I2C instance + I2C Address + channel (A-D)'
"""

from enum import IntEnum, StrEnum
from dataclasses import dataclass
from types import MappingProxyType
from typing import Dict, List, Tuple, NamedTuple

# the ACB board has 3 I2C networks, 8 DAC's per I2C network (24 total DAC's == 96 channels) 
class I2CInstance(IntEnum):
    _0 = 0,
    _1 = 1,
    _2 = 2

# MCP4728 DAC's are only addressable via I2C: 0x0-0x7
class DACI2CAddress(IntEnum):
    _0 = 0
    _1 = 1
    _2 = 2
    _3 = 3
    _4 = 4
    _5 = 5
    _6 = 6
    _7 = 7

# MCP4728 DAC's each have 4 channels (A-D)
class DACChannel(StrEnum):
    VOUTA = 'A'
    VOUTB = 'B'
    VOUTC = 'C'
    VOUTD = 'D'

class DACProperties(NamedTuple):
    i2c_instance: I2CInstance
    i2c_address: DACI2CAddress 
    channel: DACChannel 

@dataclass(frozen=True)
class ACBPinMap:
    ADC_PIN_TO_DAC: Dict[str, DACProperties] = MappingProxyType({
        'SPI0_CS0_IN4': DACProperties(I2CInstance._0, DACI2CAddress._0, DACChannel.VOUTA),
        'SPI0_CS0_IN5': DACProperties(I2CInstance._0, DACI2CAddress._0, DACChannel.VOUTB),
        'SPI0_CS0_IN6': DACProperties(I2CInstance._0, DACI2CAddress._0, DACChannel.VOUTC),
        'SPI0_CS0_IN7': DACProperties(I2CInstance._0, DACI2CAddress._0, DACChannel.VOUTD),
    })

