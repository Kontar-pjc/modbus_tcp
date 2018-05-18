import sys
import logging
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp
import adapter
from endian_type import EndianType

class device:

    def __init__(self, company, product, master, data_format):
        self.company = company
        self.product = product
        self.master = master
        self.data_format = data_format
        self.adapter16 = None
        self.adapter32 = None
        self.get_adapter()

    def get_adapter(self):
        adapters = adapter.Adapter.__subclasses__()
        for adap in adapters:
            instance = adap()
            if(instance.endian_type == self.data_format and instance.length == 2):
                self.adapter16 = instance
            if(instance.endian_type == self.data_format and instance.length == 4):
                self.adapter32 = instance
        print(self.adapter16,self.adapter32)
        pass
    
    def read_holding_register(self, id, register_start, register_quantity):
        data = self.master.execute(id, cst.READ_HOLDING_REGISTERS, register_start, register_quantity)
        return self.adapter16.perform(data)

if __name__ == "__main__":
    try:
        MASTER = modbus_tcp.TcpMaster(host="192.168.0.109", port=1100)
        MASTER.set_timeout(5.0)
        input_value = (14,20,60,80)
        xiaomi_light = device("xiaomi", "light", MASTER, EndianType.LittleEndian.value)
        print(xiaomi_light.read_holding_register(1,0,4))
    except modbus_tk.modbus.ModbusError as err:
        pass