import ftd2xx
from typing import Optional

class FTD2XXI2C:
    def __init__(self):
        self.device = None
        self.locked = False
        self._setup_device()

    def _setup_device(self):
        # Find and open first FTDI device
        num_devices = ftd2xx.createDeviceInfoList()
        if num_devices == 0:
            raise RuntimeError("No FTDI devices found")

        # Open the device
        self.device = ftd2xx.open(0)

        # Configure for I2C
        self.device.setBitMode(0xFF, 0x00)  # Reset
        self.device.setBitMode(0xFF, 0x02)  # MPSSE mode

        # Configure as I2C master
        self.device.write(b'\x8A\x97\x8D')  # Disable clock divide by 5, turn off loopback, enable 3-phase
        self.device.write(b'\x86\x00\x00')  # Set clock frequency (100kHz)

    def try_lock(self) -> bool:
        if not self.locked:
            self.locked = True
            return True
        return False

    def unlock(self) -> None:
        self.locked = False

    def writeto(self, address: int, buffer: bytes, *, start: int = 0, end: Optional[int] = None, stop: bool = True) -> None:
        """
        Writes data to an I2C device from the given buffer.
        :param address: The I2C address of the device.
        :param buffer: The buffer containing data to write.
        :param start: The starting index in the buffer.
        :param end: The ending index in the buffer.
        :param stop: Whether to send a stop condition after writing.
        """
        if end is None:
            end = len(buffer)
        # Create a memoryview for slicing
        sliced_buffer = memoryview(buffer)[start:end]

        # Send start condition and the address with write flag
        self.device.write(b'\x80' + bytes([(address << 1)]))

        # Write the sliced buffer
        self.device.write(bytes(sliced_buffer))

        if stop:
            # Send a stop condition
            self.device.write(b'\x87')  # Stop command
                                                                                

    def readfrom_into(self, address: int, buffer: bytearray, *, start: int = 0, end: Optional[int] = None, stop: bool = True) -> None:
        """
        Reads data from an I2C device into the given buffer.
        :param address: The I2C address of the device.
        :param buffer: The buffer to store the data.
        :param start: The starting index in the buffer.
        :param end: The ending index in the buffer.
        :param stop: Whether to send a stop condition after reading.
        """
        if end is None:
            end = len(buffer)
        # Create a memoryview for slicing
        sliced_buffer = memoryview(buffer)[start:end]
        length = len(sliced_buffer)

        # Send start condition and the address with read flag
        self.device.write(b'\x80' + bytes([(address << 1) | 0x01]))

        # Read the specified number of bytes
        read_data = bytearray()
        while len(read_data) < length:
            chunk = self.device.read(length - len(read_data))
            if not chunk:
                raise RuntimeError("Timeout while reading from I2C device")
            read_data.extend(chunk)

        # Copy the read data into the sliced buffer
        sliced_buffer[:] = read_data[:length]

        if stop:
            # Send a stop condition
            self.device.write(b'\x87')  # Stop command



    def scan(self):
        """Scan for I2C devices"""
        found_devices = []
        for address in range(0x08, 0x78):
            try:
                self.writeto(address, b'', stop=True)
                found_devices.append(address)
            except:
                pass
        return found_devices
