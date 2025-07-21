import socket
import threading

class Client:
    def __init__(self, server_ip=None, server_port=None, on_message=None):
        """
        :param on_message: 回调函数，接收参数 (message: str)
        """
        self.server_ip = server_ip or input("请输入服务器IP: ")
        self.server_port = server_port or int(input("请输入服务器端口: "))
        self.on_message = on_message
        if not callable(self.on_message):
            raise ValueError("on_message 必须是一个可调用的函数")
        self.running = True

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.server_ip, self.server_port))
        print(f"已连接服务器 {self.server_ip}:{self.server_port}")

        # 启动接收消息线程
        self.receiver_thread = threading.Thread(target=self.receive_messages, daemon=True)
        self.receiver_thread.start()

    def set_on_message(self, callback):
        """
        设置接收消息的回调函数
        :param callback: 回调函数，接收参数 (message: str)
        """
        self.on_message = callback
        if not callable(self.on_message):
            raise ValueError("on_message 必须是一个可调用的函数")
        
    def receive_messages(self):
        """
        后台接收服务器消息并调用回调
        """
        try:
            while self.running:
                data = self.sock.recv(1024)
                if not data:
                    print("⚠️ 服务器已断开连接")
                    break
                msg = data.decode().strip()
                if self.on_message:
                    self.on_message(msg)  # 调用回调
        except Exception as e:
            print(f"⚠️ 接收线程异常: {e}")
        finally:
            self.running = False
            self.sock.close()

    def send(self, msg):
        """
        发送消息到服务器
        """
        try:
            self.sock.sendall(msg.encode())
        except Exception as e:
            print(f"❌ 发送失败: {e}")

    def close(self):
        """
        关闭连接
        """
        self.running = False
        self.sock.close()
        print("✅ 客户端已关闭")

if __name__ == "__main__":
    # 🎯 使用示例
    def handle_message(msg):
        print(f"📩 收到服务器消息: {msg}")
        if msg.startswith("INPUT"):
            user_input = input("> ")
            client.send(user_input)

    client = Client(on_message=handle_message)

    # 主线程可随时发送消息
    try:
        while client.running:
            text = input("你想发送到服务器的消息 (或 quit 退出): ")
            if text.lower() == "quit":
                break
            client.send(text)
    finally:
        client.close()
