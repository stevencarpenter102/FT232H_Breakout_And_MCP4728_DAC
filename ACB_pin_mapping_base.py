"""
The ACB has ADC pins (from ADC128S102 chips on-board) exposed to the outside world.
To control the voltages on these pins, MCP4728 DAC's have been connected to each channel's input.
This files contains the mapping for 'ADC pins'---->'DAC's I2C instance + I2C Address + channel (A-D)'
"""

import os

# not sure if this should be here...or needs to be done command line?
os.environ['BLINKA_FT232H'] = '1'  # Enable FT232H

import board
from enum import IntEnum, StrEnum
from dataclasses import dataclass
from types import MappingProxyType
from typing import Dict, NamedTuple
import collections
import adafruit_mcp4728
import adafruit_tca9548a

# the ACB board has 3 I2C networks, 8 DAC's per I2C network (24 total DAC's == 96 channels) 
class I2CInstance(IntEnum):
    _0 = 0,
    _1 = 1,
    _2 = 2

# MCP4728 DAC's are only addressable via I2C: 0x0-0x7
class DACI2CAddress(IntEnum):
    _0 = 0x60
    _1 = 0x61
    _2 = 0x62
    _3 = 0x63
    _4 = 0x64
    _5 = 0x65
    _6 = 0x66
    _7 = 0x67

# MCP4728 DAC's each have 4 channels (A-D)
class DACChannel(IntEnum):
    VOUTA = 0 
    VOUTB = 1 
    VOUTC = 2 
    VOUTD = 3 

class DACProperties(NamedTuple):
    i2c_instance: I2CInstance
    i2c_address: DACI2CAddress 
    channel: DACChannel 

@dataclass(frozen=True)
class ACBPinMap:
    ADC_PIN_TO_DAC: Dict[str, DACProperties] = MappingProxyType({
        'SPI0_CS0_IN4': DACProperties(I2CInstance._0, DACI2CAddress._1, DACChannel.VOUTA),
        'SPI0_CS0_IN5': DACProperties(I2CInstance._0, DACI2CAddress._1, DACChannel.VOUTB),
        'SPI0_CS0_IN6': DACProperties(I2CInstance._0, DACI2CAddress._1, DACChannel.VOUTC),
        'SPI0_CS0_IN7': DACProperties(I2CInstance._0, DACI2CAddress._1, DACChannel.VOUTD),
    })

# Create a nested dictionary structure to hold DAC (P/N: MCP4728) objects
class DACArray:
    def __init__(self):
        # TCA9548A i2c multiplexer used since MCP4728 DAC's are >>8 in quantity, but only have up to 8 memory addresses 
        self.i2c = board.I2C()
        self.i2c_multiplexed = adafruit_tca9548a.TCA9548A(self.i2c)

        # Define I2C buses for each network
        self.I2C_BUSES = {
            I2CInstance._0: self.i2c_multiplexed[0],
            I2CInstance._1: self.i2c_multiplexed[1],
            I2CInstance._2: self.i2c_multiplexed[2]   # can go up to 8 total instance for TCA9548A i2c multiplexer part 
        }

        # define collection of DAC's
        self.dacs = collections.defaultdict(
            lambda: collections.defaultdict(dict)
        )

        self._initialize_dacs()

    def _initialize_dacs(self):
        # Iterate through all combinations and create DAC objects
        for i2c_inst in I2CInstance:
            i2c = self.I2C_BUSES[i2c_inst]
            for addr in DACI2CAddress:
                try:
                    dac = adafruit_mcp4728.MCP4728(i2c, address=addr)
                    self.dacs[i2c_inst][addr] = {
                        DACChannel.VOUTA: dac.channel_a,
                        DACChannel.VOUTB: dac.channel_b,
                        DACChannel.VOUTC: dac.channel_c,
                        DACChannel.VOUTD: dac.channel_d
                    }
                    print(f"Initialize DAC at I2C{i2c_inst}, address {hex(addr)}")
                except ValueError as e:
                    print(f"Failed to initialize DAC at I2C{i2c_inst}, address {hex(addr)}: {e}")

    def get_dac_channel(self, pin_name: str):
        """
        Get DAC channel instance based on pin name from ACBPinMap
        
        Args:
            pin_name: String key from ACBPinMap.ADC_PIN_TO_DAC mapping
            
        Returns:
            DAC channel instance
            
        Raises:
            KeyError: If pin_name not found in mapping or DAC not initialized
        """
        try:
            # Look up DAC properties from pin map
            dac_props = ACBPinMap.ADC_PIN_TO_DAC[pin_name]
            
            # Get corresponding DAC channel from dacs array using properties
            return self.dacs[dac_props.i2c_instance][dac_props.i2c_address][dac_props.channel]
            
        except KeyError:
            raise KeyError(f"No DAC found for pin {pin_name}")


# Example usage:
if __name__ == "__main__":
    dac_array = DACArray()    

    pin_mapping_OAHU = {'OAHU_Current_5V':'SPI0_CS0_IN4',
                        'Trigger_Current_12V':'SPI0_CS0_IN5',
                        'Trigger_Current_5V':'SPI0_CS0_IN6',
                        'Solenoid_Current':'SPI0_CS0_IN7'}

    def oahu_current_amps_to_dac_units(amps: float) -> float:
        # example: dac_setpoint [normalized: 0.0-1.0] = (amps / max_measurable_amps)
        return amps / 5

    try:
        dac = dac_array.get_dac_channel(pin_mapping_OAHU['OAHU_Current_5V'])

        dac.normalized_value = oahu_current_amps_to_dac_units(3.0)  # 1.0A is = 1.0V @DAC pin (assuming DAC_Ref = 5.0V)
    except KeyError as e:
        print(f"Error: {e}")
