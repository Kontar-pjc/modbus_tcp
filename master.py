#!/usr/bin/env python
# -*- coding: utf_8 -*-
import sys
import logging
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp
import adapter
LOGGER = modbus_tk.utils.create_logger("console")

if __name__ == "__main__":
    try:
        #连接从机地址,这里要注意端口号和IP与从机一致
        MASTER = modbus_tcp.TcpMaster(host="192.168.0.109", port=1100)
        MASTER.set_timeout(5.0)
        LOGGER.info("connected")
#        input_value = (14,20,60,80)
#        input_adapter = adapter.adapter16little(input_value)
#        MASTER.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 0, output_value=input_adapter.perform())
        MASTER.execute(1, cst.WRITE_MULTIPLE_REGISTERS, starting_address=5, output_value=[333333333333333.5],data_format='>f')
#        data = MASTER.execute(1, cst.READ_HOLDING_REGISTERS, 0, 4)
#        adapter = adapter.adapter16little(data)
#        print(adapter.perform())
        #读取从机1的4-14保持寄存器，因为寄存器独立分块了，所以不能直接连通读取，强行结果是会出现数据越界
#        LOGGER.info(MASTER.execute(1, cst.READ_HOLDING_REGISTERS, 0, 14))
        # 需要按照execute格式
#        LOGGER.info(MASTER.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 0, output_value=[0, 1, 2]))
#        LOGGER.info(MASTER.execute(1, cst.READ_HOLDING_REGISTERS, 0, 4))

        # LOGGER.info(MASTER.execute(2, cst.READ_COILS, 0, 8))
        # LOGGER.info(MASTER.execute(2, cst.WRITE_MULTIPLE_COILS, 0, output_value=[1, 0, 0, 0, 1]))
        # LOGGER.info(MASTER.execute(2, cst.READ_COILS, 0, 8))
        # LOGGER.info(MASTER.execute(2, cst.READ_HOLDING_REGISTERS, 0, 4))
        # 线圈和寄存器地址不是同一区块的
    except modbus_tk.modbus.ModbusError as err:
        LOGGER.error("%s- Code=%d" % (err, err.get_exception_code()))