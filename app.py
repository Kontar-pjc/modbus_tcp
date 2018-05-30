from endian_type import EndianType
from device import device
from controller import DeviceController
import adapter

def sys_output():
    return """
    ---------- Modbus/TCP Adapter   ---------
    ---------- 1.List Devices added ---------
    ---------- 2.Add New Device     ---------
    """

if __name__ == "__main__":
    conntroller = DeviceController()
    res = input(sys_output())
    if (res == 1):
        conntroller.list_devices()
    elif (res == '2'):
        conntroller.append()
    else:
        pass