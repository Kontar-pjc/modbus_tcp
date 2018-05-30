import adapter
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_tcp, hooks
from device import device
from endian_type import EndianType
import struct


# convert float to hex storage format,and then convert to int.
def f2hex(f):
    hex_str = hex(struct.unpack('<I', struct.pack('<f', f))[0])
    return int(hex_str,0)

# convert double to hex storage format,and then convert to int.
def d2hex(f):
    hex_str = hex(struct.unpack('<Q', struct.pack('<d', f))[0])
    return int(hex_str,0)

if __name__ == "__main__":
    ada = adapter.adapter_CDAB()
    master = modbus_tcp.TcpMaster(host="localhost", port=502)
#    master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 0, output_value = ada.format(f2hex(3.14)))
#    master.execute(1, cst.READ_HOLDING_REGISTERS, 0, 1)
    data_format = {
        'int': EndianType.AB.value,
        'long': EndianType.ABCD.value,
        'float': EndianType.ABCD.value,
        'double': EndianType.ABCDEFGH.value
    }
    data_format2 = {
        'int': EndianType.BA.value,
        'long': EndianType.CDAB.value,
        'float': EndianType.CDAB.value,
        'double': EndianType.GHEFCDAB.value
    }
    dev = device("","","localhost",502,1,data_format)
    dev2 = device("","","localhost",502,2,data_format2)
    print(dev.read_int(0,1))
    print(dev2.read_int(0,1))
    print(dev.read_long(1,2))
    print(dev2.read_long(1,2))
    print(dev.read_float(3,2))
    print(dev2.read_float(3,2))