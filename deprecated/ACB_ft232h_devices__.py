from pyftdi.usbtools import UsbTools
from pyftdi.ftdi import Ftdi
import usb.core
import usb.util

def list_ftdi_devices():
    """
    List all connected FTDI devices and their serial numbers.
    """
    try:
        # FTDI default vendor ID and product ID
        VENDOR_ID = 0x0403
        PRODUCT_ID = 0x6014  # Default for FT232H
        
        # Find the device
        device = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
        
        if device is None:
            print("No FTDI devices found")
            return
            
        # Get device information
        try:
            manufacturer = usb.util.get_string(device, device.iManufacturer)
            serial = usb.util.get_string(device, device.iSerialNumber)
            product = usb.util.get_string(device, device.iProduct)
            
            print(f"\nDevice Information:")
            print(f"Manufacturer: {manufacturer}")
            print(f"Serial Number: {serial}")
            print(f"Product: {product}")
            print(f"Bus: {device.bus}")
            print(f"Address: {device.address}")
            
        except Exception as e:
            print(f"Found device but couldn't read string descriptors: {str(e)}")
            print(f"Raw device info:")
            print(f"Vendor ID: 0x{device.idVendor:04x}")
            print(f"Product ID: 0x{device.idProduct:04x}")
            
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        
if __name__ == "__main__":
    try:
        list_ftdi_devices()
    except Exception as e:
        print(f"Failed to initialize FTDI device list: {str(e)}")