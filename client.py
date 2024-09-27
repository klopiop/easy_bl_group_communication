import bluetooth

def start_client(server_mac_address):
    """启动客户端并连接到服务器"""
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    port = bluetooth.PORT_ANY  # 自动选择可用的 RFCOMM 端口
    try:
        sock.connect((server_mac_address, port))
        print("已连接到服务器")

        while True:
            message = input("你: ")
            if message.lower() == 'exit':
                break
            sock.send(message.encode('utf-8'))

            # 接收来自服务器的消息
            data = sock.recv(1024)
            print(f"收到消息: {data.decode('utf-8')}")
    except Exception as e:
        print(f"连接到服务器失败: {e}")
    finally:
        sock.close()

def list_devices():
    """扫描并列出附近的蓝牙设备"""
    print("正在扫描附近的蓝牙设备...")
    devices = bluetooth.discover_devices(lookup_names=True)
    device_list = []
    
    for index, (addr, name) in enumerate(devices):
        print(f"{index}: {name} - {addr}")
        device_list.append((addr, name))
    
    return device_list

if __name__ == "__main__":
    # 初次扫描设备
    device_list = list_devices()

    if not device_list:
        print("未找到任何蓝牙设备，程序退出。")
    else:
        while True:
            choice = input("请输入要连接的设备序号，或输入 'exit' 退出，输入 'refresh' 刷新: ")
            if choice.lower() == 'exit':
                break
            elif choice.lower() == 'refresh':
                device_list = list_devices()
                if not device_list:
                    print("未找到任何蓝牙设备，继续扫描...")
            else:
                try:
                    choice = int(choice)
                    if 0 <= choice < len(device_list):
                        server_mac = device_list[choice][0]  # 获取选定设备的 MAC 地址
                        start_client(server_mac)
                        break
                    else:
                        print("无效选择，请重新输入。")
                except ValueError:
                    print("请输入有效的序号。")
