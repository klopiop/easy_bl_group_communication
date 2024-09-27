import sys
from server import start_server
from client import start_client

def main():
    """主菜单，用于选择创建服务器还是加入服务器"""
    print("欢迎来到蓝牙聊天室")
    print("1. 创建聊天室 (服务器)")
    print("2. 加入聊天室 (客户端)")
    choice = input("请选择操作 (1/2): ")

    if choice == '1':
        print("创建服务器...")
        start_server()
    elif choice == '2':
        server_mac = input("请输入服务器的 MAC 地址: ")
        print(f"正在连接到 {server_mac}...")
        start_client(server_mac)
    else:
        print("无效选择，程序退出。")
        sys.exit(0)

if __name__ == "__main__":
    main()
