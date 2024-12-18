from opcua import Server
import random
import time

# 创建 OPC UA 服务器
server = Server()

# 设置服务器地址和端口
server.set_endpoint("opc.tcp://0.0.0.0:4840")

# 创建一个命名空间，建议使用自定义的 URN
uri = "http://example.org"
idx = server.register_namespace(uri)

# 获取服务器对象并添加一个对象
objects = server.nodes.objects
device = objects.add_object(idx, "Device1")

# 创建1000个变量
variables = []
for i in range(5000):  # 创建1000个变量
    variable = device.add_variable(idx, f"Tag_{i}", random.random())
    variable.set_writable()  # 使变量可写
    variables.append(variable)

# 启动服务器
server.start()
print("Server started at {}".format(server.endpoint))

try:
    while True:
        # 每秒更新一次所有变量的值
        for var in variables:
            new_value = random.random()  # 随机更新变量值
            var.set_value(new_value)  # 设置新值
            print(f"Updated {var.nodeid} to {new_value}")  # 输出更新的值
        time.sleep(2)  # 每秒更新一次

except KeyboardInterrupt:
    # 停止服务器
    print("Server stopping...")
    server.stop()
