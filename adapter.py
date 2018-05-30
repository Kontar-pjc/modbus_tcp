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

class adapter_AB(Adapter):
    # 0xAB 存储为 0xAB 的情况
    # 一个寄存器存储一个16bit的整型的情况
    def __init__(self):
        # 两个字节，len(data) = 1
        super().__init__(2, EndianType.AB.value)

    def perform(self, data):
        return list(data)

    def check(self):
        pass

class adapter_BA(Adapter):
    # 0xAB 存储为 0xBA 的情况
    # 一个寄存器存储一个16bit的整型的情况
    def __init__(self):
        super().__init__(2, EndianType.BA.value)

    def perform(self, data):
        res = []
        for each in data:
            temp = each<<8 & 0xffff | each>>8
            res.append(temp)
        return res

    def check(self):
        pass

class adapter_ABCD(Adapter):
    # 0xABCD 存储为 0xABCD 的情况
    # 两个寄存器存储一个32bit的整型的情况
    # 2个data值返回一个整型值
    def __init__(self):
        # 两个字节，len(data) = 1
        super().__init__(4, EndianType.ABCD.value)

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

class adapter_CDAB(Adapter):
    # 0xABCD 存储为 0xCDAB 的情况
    # 两个寄存器存储一个32bit的整型的情况
    # 2个data值返回一个整型值
    def __init__(self):
        # 两个字节，len(data) = 1
        super().__init__(4, EndianType.CDAB.value)

    def perform(self, data):
        self.check(data)
        even_fun = lambda x: not x % 2
        even = filter(even_fun, range(len(data)-1))
        res = []
        for i in even:
            temp = data[i+1]<<16 | data[i]
            res.append(temp)
        return res

    def check(self, data):
        return len(data)%2 == 0

    # input data: 0xABCD
    # return: [0xCD, 0xAB]
    def format(self, data):
        return [data&0x0000ffff, data>>16]
        
class adapter_DCBA(Adapter):
    # 0xABCD 存储为 0xDCBA 的情况
    # 两个寄存器存储一个32bit的整型的情况
    # data是16bit的值，return 32bit的整型
    def __init__(self):
        super().__init__(4, EndianType.DCBA.value)

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

class adapter_ABCDEFGH(Adapter):
    # 0xABCDEFGH 存储为 0xABCDEFGH 的情况
    # 四个寄存器存储一个64bit的整型的情况
    # 4个data值返回一个double类型值
    def __init__(self):
        # 两个字节，len(data) = 1
        super().__init__(8, EndianType.ABCDEFGH.value)

    def perform(self, data):
        self.check(data)
        even_fun = lambda x: not x % 4
        even = filter(even_fun, range(len(data)-1))
        res = []
        for i in even:
            temp = data[i]<<48 | data[i+1]<<32 | data[i+2]<<16 | data[i+3]
            res.append(temp)
        return res

    def check(self, data):
        return len(data)%4 == 0

class adapter_GHEFCDAB(Adapter):
    # 0xABCDEFGH 存储为 0xGHEFCDAB 的情况
    # 两个寄存器存储一个32bit的整型的情况
    # data是16bit的值，return 32bit的整型
    def __init__(self):
        super().__init__(8, EndianType.GHEFCDAB.value)

    def perform(self, data):
        self.check(data)
        # 定义一个判断时候是偶数的函数
        even_fun = lambda x: not x % 4
        even = filter(even_fun, range(len(data)-1))
        res = []
        for i in even:
            temp = data[i+3]<<48 | data[i+2]<<32 | data[i+1]<<16 | data[i]
            res.append(temp)
        return res

    def check(self, data):
        return len(data)%4 == 0

class adapter_HGFEDCBA(Adapter):
    # 0xABCDEFGH 存储为 0xHGFEDCBA 的情况
    # 两个寄存器存储一个32bit的整型的情况
    # data是16bit的值，return 32bit的整型
    def __init__(self):
        super().__init__(8, EndianType.HGFEDCBA.value)

    def perform(self, data):
        self.check(data)
        temp_list = []
        for each in data:
            temp = each<<8 & 0xffff | each>>8
            temp_list.append(temp)
        # 定义一个判断时候是偶数的函数
        even_fun = lambda x: not x % 4
        even = filter(even_fun, range(len(data)-1))
        res = []
        for i in even:
            temp = temp_list[i+3]<<48 | temp_list[i+2]<<32 | temp_list[i+1]<<16 | temp_list[i]
            res.append(temp)
        return res

    def check(self, data):
        return len(data)%4 == 0
