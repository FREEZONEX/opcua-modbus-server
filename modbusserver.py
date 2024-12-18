import random
import threading
import time
from pymodbus.server.sync import StartTcpServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext, ModbusSequentialDataBlock
from pymodbus.device import ModbusDeviceIdentification

NUM_DEVICES = 250  # 模拟设备数量


def generate_initial_registers(num_devices):
    """
    生成初始保持寄存器数据，每个设备的寄存器地址从 0 到 9。
    """
    slaves = {}
    for slave_id in range(1, num_devices + 1):
        # 初始化 10 个保持寄存器（地址范围 0-9）
        initial_values = [random.randint(0, 65535) for _ in range(10)]
        slaves[slave_id] = ModbusSlaveContext(
            hr=ModbusSequentialDataBlock(0, initial_values),
            ir=ModbusSequentialDataBlock(0, [0] * 10),
            co=ModbusSequentialDataBlock(0, [0] * 10),
            di=ModbusSequentialDataBlock(0, [0] * 10)
        )
    return slaves


def update_registers(context, num_devices, interval=1):
    """
    定期更新每个设备的保持寄存器，模拟实时数据变化。
    """
    while True:
        for slave_id in range(1, num_devices + 1):
            try:
                slave_context = context[slave_id]
                # 更新寄存器地址 0 到 9 的值
                for register_address in range(10):
                    new_value = [random.randint(0, 65535)]
                    slave_context.setValues(3, register_address, new_value)
                    print(f"设备 {slave_id} 地址 {register_address} 更新为：{new_value[0]}")
            except Exception as e:
                print(f"更新设备 {slave_id} 时发生错误：{e}")
        time.sleep(interval)


def setup_server_context(num_devices):
    """
    初始化Modbus服务器上下文，包含多个从设备。
    """
    slaves = generate_initial_registers(num_devices)
    return ModbusServerContext(slaves=slaves, single=False)


def setup_server_identity():
    """
    设置Modbus服务器的设备标识信息。
    """
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'Pymodbus'
    identity.ProductCode = 'PM'
    identity.VendorUrl = 'http://github.com/riptideio/pymodbus/'
    identity.ProductName = 'Pymodbus Server'
    identity.ModelName = 'Pymodbus Server'
    identity.MajorMinorRevision = '2.5.3'
    return identity


def start_modbus_server():
    context = setup_server_context(NUM_DEVICES)
    identity = setup_server_identity()

    updater_thread = threading.Thread(target=update_registers, args=(context, NUM_DEVICES), daemon=True)
    updater_thread.start()

    print(f"启动 Modbus TCP 服务器，监听地址 0.0.0.0:5020，模拟 {NUM_DEVICES} 个设备...")
    StartTcpServer(context=context, identity=identity, address=("0.0.0.0", 5020))


if __name__ == "__main__":
    start_modbus_server()
