from device import device
from endian_type import EndianType
import adapter
import struct

class DeviceController:
    def __init__(self):
        self.device_list = list()

    def list_devices(self):
        for each in self.device_list:
            print(each.to_string())

    def append(self):
        ip = input("New device's IP address:")
        port = int(input("New device's port:"))
        device_id = int(input("New device's id:"))
        company = input("New device's company:")
        product = input("New device's name:")
        dev = device(company, product, ip, port, device_id, self.data_format_output())
        self.device_list.append(dev)
        

    def data_format_output(self):
        data_format = {
            'int': EndianType.AB.value,
            'long': EndianType.ABCD.value,
            'float': EndianType.ABCD.value,
            'double': EndianType.ABCDEFGH.value
        }
        res = input("1. Do you know the data storage format? y/n")
        if(res.lower()=='y'):
            data_format['int'] = {'1':EndianType.AB.value,
                                        '2':EndianType.BA.value
                                    }.get(input("Int: 1.AB  2.BA    "),1)
            data_format['long'] = {'1':EndianType.ABCD.value,
                                   '2':EndianType.CDAB.value,
                                   '3':EndianType.DCBA.value
                                  }.get(input("Long: 1.ABCD  2.CDAB  3.DCBA    "),1)
            data_format['float'] = {'1':EndianType.ABCD.value,
                                    '2':EndianType.CDAB.value,
                                    '3':EndianType.DCBA.value
                                   }.get(input("Float: 1.ABCD  2.CDAB  3.DCBA    "),1)
            data_format['double'] = {'1':EndianType.ABCDEFGH.value,
                                     '2':EndianType.GHEFCDAB.value,
                                     '3':EndianType.HGFEDCBA.value
                                    }.get(input("Float: 1.ABCDEFGH  2.GHEFCDAB  3.HGFEDCBA    "),1)
        elif(res.lower()=='n'):
            self.def_data_format_auto()
        else:
            print("Wrong input,use the default endian type: Big-Endian!")
        return data_format

    def def_data_format_auto(self):
        instaces = adapter.Adapter.__subclasses__()
        for instance in instaces:
            pass
        pass
        