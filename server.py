import bluetooth
import threading

clients = []  # 用于保存所有连接的客户端

def broadcast_message(message, sender_socket):
    """广播消息给所有客户端，除了发送者"""
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                clients.remove(client)

def handle_client(client_socket):
    """处理单个客户端的消息"""
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                print(f"收到消息: {message.decode('utf-8')}")
                broadcast_message(message, client_socket)
        except:
            print("客户端断开连接")
            clients.remove(client_socket)
            client_socket.close()
            break

def start_server():
    """启动蓝牙服务器"""
    server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    try:
        server_socket.bind(("", bluetooth.PORT_ANY))
        server_socket.listen(5)
        port = server_socket.getsockname()[1]
        print(f"蓝牙聊天室服务器已启动，监听端口: {port}")

        # 获取本机蓝牙地址
        local_address = server_socket.getsockname()[0]  # 获取绑定的地址
        print(f"本机蓝牙 MAC 地址: {local_address}")

        bluetooth.advertise_service(server_socket, "BluetoothChatServer",
                                    service_classes=[bluetooth.SERIAL_PORT_CLASS],
                                    profiles=[bluetooth.SERIAL_PORT_PROFILE])

        while True:
            client_socket, client_info = server_socket.accept()
            print(f"新客户端连接: {client_info}")
            clients.append(client_socket)

            # 每个客户端开启一个线程来处理消息
            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.start()
    except Exception as e:
        print(f"启动服务器时发生错误: {e}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()
