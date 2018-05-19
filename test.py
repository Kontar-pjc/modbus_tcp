import sys
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp
from endian_type import EndianType
from device import device

if __name__ == "__main__":
    try:
        MASTER = modbus_tcp.TcpMaster(host="192.168.0.110", port=502)
        MASTER.set_timeout(5.0)
        input_value = (14,20,60,80)
        xiaomi_light = device("xiaomi", "light", MASTER, EndianType.LittleEndian.value)
        print(hex(xiaomi_light.read_holding_register(1,5,2)[0]))
    except modbus_tk.modbus.ModbusError as err:
        pass