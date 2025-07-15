import socket
import threading

class Server:
    def __init__(self, host='0.0.0.0', port=12345):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.server.listen(2)
        self.port = self.server.getsockname()[1]
        print(f"服务器启动: {host}:{self.port}")

        self.players = {}  # player_id -> (conn, addr)
        self.lock = threading.Lock()
        self.running = True

        # 游戏内核回调
        self.on_game_start = None
        self.on_player_disconnect = None
        self.on_player_input = None

    def start(self):
        threading.Thread(target=self.accept_players, daemon=True).start()

    def accept_players(self):
        while len(self.players) < 2 and self.running:
            conn, addr = self.server.accept()
            player_id = len(self.players) + 1
            self.players[player_id] = (conn, addr)
            print(f"玩家 {player_id} 已连接: {addr}")
            conn.sendall(f"欢迎 Player {player_id}\n".encode())

            threading.Thread(target=self.handle_player, args=(player_id,), daemon=True).start()

        if len(self.players) == 2 and self.on_game_start:
            self.on_game_start()

    def handle_player(self, player_id):
        conn, addr = self.players[player_id]
        try:
            while self.running:
                data = conn.recv(1024)
                if not data:
                    break
                msg = data.decode().strip()
                print(f"[Player {player_id}] {msg}")
                if self.on_player_input:
                    self.on_player_input(player_id, msg)
        except:
            pass
        finally:
            if self.running and self.on_player_disconnect:
                self.on_player_disconnect(player_id)
            self.stop()

    # API
    def send_to_player(self, player_id, msg):
        if player_id in self.players:
            conn, _ = self.players[player_id]
            conn.sendall(msg.encode())

    def broadcast(self, msg):
        for pid in self.players:
            self.send_to_player(pid, msg)

    def get_player_handle(self, player_id):
        return self.players.get(player_id)

    def stop(self):
        if not self.running:
            return
        self.running = False
        for conn, _ in self.players.values():
            conn.close()
        self.server.close()
        print("服务器已关闭")

# === 示例 ===
if __name__ == "__main__":
    def game_start():
        print("🎮 游戏开始")
        server.broadcast("GAME_START")

    def player_input(player_id, msg):
        print(f"玩家 {player_id} 输入: {msg}")
        # 示例: echo 回去
        server.send_to_player(player_id, f"你输入了: {msg}")

    def player_disconnect(player_id):
        print(f"❌ 玩家 {player_id} 断开连接（判定投降）")
        server.broadcast("GAME_OVER 投降")

    server = Server()
    server.on_game_start = game_start
    server.on_player_input = player_input
    server.on_player_disconnect = player_disconnect
    server.start()

    input("按 Enter 关闭服务器...\n")
    server.stop()
