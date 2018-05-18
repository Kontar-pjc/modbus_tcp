from endian_type import EndianType

class Adapter:

    # 该类为解析适配器类，即从寄存器中读取数据，将其按照相应的字节序进行解析
    def __init__(self, length, endian_type):
        # adapter处理的字节数
        self.length = length
        # 定义处理的类型
        self.endian_type = endian_type

    def perform(self, data):
        pass

    def check(self):
        pass
    
#    def length(self):
#        return self.length

#    def endian_type(self):
#        return self.type

class adapter16big(Adapter):
    # 0x1234 存储为 0x12 0x34 的情况
    # 一个寄存器存储一个16bit的整型的情况
    def __init__(self):
        # 两个字节，len(data) = 1
        super().__init__(2, EndianType.BigEndian.value)

    def perform(self, data):
        return list(data)

    def check(self):
        pass

class adapter16little(Adapter):
    # 0x1234 存储为 0x34 0x12 的情况
    # 一个寄存器存储一个16bit的整型的情况
    def __init__(self):
        super().__init__(2, EndianType.LittleEndian.value)

    def perform(self, data):
        res = []
        for each in data:
            temp = each<<8 & 0xffff | each>>8
            res.append(temp)
        return res

    def check(self):
        pass

class adapter32big(Adapter):
    # 0x12345678 存储为 0x12 0x34 0x56 0x78 的情况
    # 两个寄存器存储一个32bit的整型的情况
    # 2个data值返回一个整型值
    def __init__(self):
        # 两个字节，len(data) = 1
        super().__init__(4, EndianType.BigEndian.value)

    def perform(self, data):
        self.check(data)
        even_fun = lambda x: not x % 2
        even = filter(even_fun, range(len(data)-1))
        res = []
        for i in even:
            temp = data[i]<<16 | data[i+1]
            res.append(temp)
        return res

    def check(self, data):
        return len(data)%2 == 0

class adapter32little(Adapter):
    # 0x12345678 存储为 0x78 0x56 0x34 0x12 的情况
    # 两个寄存器存储一个32bit的整型的情况
    # data是16bit的值，return 32bit的整型
    def __init__(self):
        super().__init__(4, EndianType.LittleEndian.value)

    def perform(self, data):
        self.check(data)
        temp_list = []
        for each in data:
            temp = each<<8 & 0xffff | each>>8
            temp_list.append(temp)
        # 定义一个判断时候是偶数的函数
        even_fun = lambda x: not x % 2
        even = filter(even_fun, range(len(data)-1))
        res = []
        for i in even:
            temp = temp_list[i] | temp_list[i+1]<<16
            res.append(temp)
        return res

    def check(self, data):
        return len(data)%2 == 0