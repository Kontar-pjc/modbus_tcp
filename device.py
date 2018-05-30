import sys
import logging
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp
import adapter
from endian_type import EndianType
import struct
LOGGER = modbus_tk.utils.create_logger("console")

class device:

    def __init__(self, company, product, ip, port_num, device_id, data_format):
        self.company = company
        self.product = product
        self.master = modbus_tcp.TcpMaster(host=ip, port=port_num)
        self.master.set_timeout(5)
        self.data_format = data_format
        self.device_id = device_id
        self.adapter_int = None
        self.adapter_long = None
        self.adapter_float = None
        self.adapter_double = None
        self.get_adapter()

    def get_adapter(self):
        adapters = adapter.Adapter.__subclasses__()
        for adap in adapters:
            instance = adap()
            if(instance.endian_type == self.data_format['int'] and instance.length == 2):
                self.adapter_int = instance
            if(instance.endian_type == self.data_format['long'] and instance.length == 4):
                self.adapter_long = instance
            if(instance.endian_type == self.data_format['float'] and instance.length == 4):
                self.adapter_float = instance
            if(instance.endian_type == self.data_format['double'] and instance.length == 8):
                self.adapter_double = instance
        print(self.adapter_int, self.adapter_long, self.adapter_float, self.adapter_double)

    # always return int
    def read_holding_register(self, register_start, register_quantity, data_type):
        try:
            data = self.master.execute(self.device_id, cst.READ_HOLDING_REGISTERS, register_start, register_quantity)
            print("raw data: " + str(data[0]))
            adapter = self.get_type_adapter(data_type)
            return adapter.perform(data)
        except modbus_tk.modbus.ModbusError as err:
            LOGGER.error("%s- Code=%d" % (err, err.get_exception_code()))

    def write_holding_register(self, starting_address, output_list, data_format):
        try:
            self.master.execute(self.device_id, cst.WRITE_MULTIPLE_REGISTERS, starting_address=starting_address, output_value=output_list, data_format=data_format)
        except modbus_tk.modbus.ModbusError as err:
            LOGGER.error("%s- Code=%d" % (err, err.get_exception_code()))
            
    def get_type_adapter(self, data_type):
        return {
            'int': self.adapter_int,
            'long': self.adapter_long,
            'float': self.adapter_float,
            'double': self.adapter_double,
        }[data_type]

    def read_int(self,register_start, register_quantity):
        return self.read_holding_register(register_start,register_quantity,'int')

    def read_long(self,register_start, register_quantity):
        return self.read_holding_register(register_start,register_quantity,'long')

    # convert int to hex, and then to float
    def read_float(self,register_start, register_quantity):
        f_list = []
        for each in self.read_holding_register(register_start,register_quantity,'float'):
            str = hex(each)[2:]
            f = struct.unpack('!f', bytes.fromhex(str))[0]
            f_list.append(f)
        return f_list

    # convert int to hex,and then to double
    def read_double(self,register_start, register_quantity):
        d_list = []
        for each in self.read_holding_register(register_start,register_quantity,'double'):
            str = hex(each)[2:]
            d = struct.unpack('!d', bytes.fromhex(str))[0]
            d_list.append(d)
        return d_list

    def to_string(self):
        print("Company: " + self.company)
        print("Product: " + self.product)
        print("Adapters for int, long, float, double: " 
            + self.adapter_int
            + self.adapter_long
            + self.adapter_float
            + self.adapter_double)
