'''
Multiple FT232H's not supported with Blinka!? Turns out not
see: https://forums.adafruit.com/viewtopic.php?t=179381 and https://github.com/adafruit/Adafruit_Blinka/issues/260
Thus, this file uses a workaround by using the pytfdi library directly &
assumes the FTD232H board has the D2XX drivers installed (https://ftdichip.com/drivers/d2xx-drivers/)
'''

import ftd2xx
from typing import Dict, List, Optional
import time

class ACBFT232HDevices:
    def __init__(self):
        self.ftdi_devices: Dict[str, ftd2xx.FTD2XX] = {}
        self.devices_info: List[Dict[str, any]] = []
        
        self._find_devices()
        self._setup_devices()

    def _find_devices(self) -> None:
        """Find all FT232H devices and store their information."""
        try:
            num_devices = ftd2xx.createDeviceInfoList()
            print(f"Found {num_devices} FTDI devices")

            if num_devices == 0:
                raise ValueError("No FT232H devices found!")

            for i in range(num_devices):
                device_info = ftd2xx.getDeviceInfoDetail(i)
                self.devices_info.append({
                    'serial': device_info['serial'].decode('ascii'),
                    'description': device_info['description'].decode('ascii'),
                    'id': device_info['id'],
                    'index': i
                })
                print(f"Found device with serial: {self.devices_info[-1]['serial']}, "
                      f"description: {self.devices_info[-1]['description']}")
                
        except Exception as e:
            print(f"Error finding devices: {e}")

    def _setup_devices(self) -> None:
        """Open and configure each FTDI device for I2C."""
        for device in self.devices_info:
            try:
                print(f"Attempting to configure device {device['serial']}")
                
                # Open the device
                ftdi = ftd2xx.open(device['index'])
                print("Device opened")
                
                # Reset the device
                ftdi.resetDevice()
                print("Device reset")
                
                # Configure the device
                try:
                    # Use positional arguments
                    ftdi.setBitMode(0xFF, 0x00)  # Reset
                    print("Reset bit mode")
                    time.sleep(0.1)  # Short delay
                    
                    ftdi.setBitMode(0xFF, 0x02)  # MPSSE mode
                    print("Set MPSSE mode")
                    time.sleep(0.1)  # Wait for all USB things to complete
                except Exception as be:
                    print(f"Bit mode error: {be}")
                    continue
                
                # Configure as I2C master
                try:
                    ftdi.write(b'\x8A\x97\x8D')  # Disable clock divide by 5, turn off loopback, enable 3-phase
                    print("Configured I2C master settings")
                    
                    # Set clock frequency (100kHz)
                    ftdi.write(b'\x86\x00\x00')  # Command to set clock divisor
                    print("Set clock frequency")
                except Exception as we:
                    print(f"Write error: {we}")
                    continue
                
                # Store the configured device
                self.ftdi_devices[device['serial']] = ftdi
                print(f"Successfully configured device {device['serial']}")
                
            except Exception as e:
                print(f"Failed to configure device {device['serial']}: {e}")
                if 'ftdi' in locals():
                    try:
                        ftdi.close()
                    except:
                        pass

    def get_device(self, serial: str) -> Optional[ftd2xx.FTD2XX]:
        """Get FTDI device by serial number."""
        return self.ftdi_devices.get(serial)

    def __del__(self):
        """Cleanup when the object is destroyed."""
        for device in self.ftdi_devices.values():
            try:
                device.close()
            except:
                pass

if __name__ == "__main__":
    try:
        # Initialize FT232H devices
        ft232h_devices = ACBFT232HDevices()
        
        # Get first device
        if ft232h_devices.devices_info:
            first_serial = ft232h_devices.devices_info[0]['serial']
            device = ft232h_devices.get_device(first_serial)
            if device:
                print(f"Successfully opened device {first_serial}")
        
    except Exception as e:
        print(f"Error: {e}")