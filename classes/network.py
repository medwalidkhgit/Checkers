import socket
import pickle
import threading
import time

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost"  # Default to localhost
        self.port = 5555
        self.addr = (self.server, self.port)
        self.player_id = None
        self.connected = False
        self.callback = None
        self.receive_thread = None
    
    def set_callback(self, callback):
        """Set a callback function that will be called when messages are received"""
        self.callback = callback
    
    def set_server(self, server_ip):
        """Set the server IP address"""
        self.server = server_ip
        self.addr = (self.server, self.port)
        print(f"[NETWORK] Server address set to: {server_ip}:{self.port}")
    
    def connect(self):
        """Connect to the server"""
        try:
            print(f"[NETWORK] Connecting to server: {self.addr}")
            self.client.connect(self.addr)
            response = self.client.recv(1024).decode()
            
            if response == "SERVER_FULL":
                print("[NETWORK] Connection rejected: Server is full")
                return None
            
            self.player_id = int(response)
            self.connected = True
            print(f"[NETWORK] Connected successfully as Player {self.player_id}")
            
            # Start receive thread
            self.receive_thread = threading.Thread(target=self.receive_messages)
            self.receive_thread.daemon = True
            self.receive_thread.start()
            
            return self.player_id
        except Exception as e:
            print(f"[NETWORK] Connection error: {e}")
            return None
    
    def disconnect(self):
        """Disconnect from the server"""
        try:
            if self.connected:
                print("[NETWORK] Disconnecting from server")
                self.connected = False
                self.client.close()
        except Exception as e:
            print(f"[NETWORK] Error during disconnect: {e}")
    
    def send_name(self, name):
        """Send player name to server"""
        try:
            print(f"[NETWORK] Sending player name: {name}")
            self.client.send(name.encode())
            return True
        except Exception as e:
            print(f"[NETWORK] Error sending name: {e}")
            self.connected = False
            return False
    
    def start_game(self):
        """Send a message to start the game"""
        message = {"type": "start_game"}
        try:
            print("[NETWORK] Sending start game request")
            self.client.send(pickle.dumps(message))
            return True
        except Exception as e:
            print(f"[NETWORK] Error sending start game: {e}")
            self.connected = False
            return False
    
    def send_move(self, board, turn):
        """Send a move update to the server"""
        message = {
            "type": "move",
            "board": board,
            "turn": turn
        }
        try:
            print(f"[NETWORK] Sending move update. Turn: {turn}")
            self.client.send(pickle.dumps(message))
            return True
        except Exception as e:
            print(f"[NETWORK] Error sending move: {e}")
            self.connected = False
            return False
    
    def receive_messages(self):
        """Continuously receive messages from the server"""
        while self.connected:
            try:
                data = self.client.recv(4096)
                if not data:
                    print("[NETWORK] Disconnected from server (no data)")
                    self.connected = False
                    break
                
                message = pickle.loads(data)
                print(f"[NETWORK] Received message of type: {message['type']}")
                
                # Call the callback function with the message
                if self.callback:
                    result = self.callback(message)
                    if result == "start_game":
                        print("[NETWORK] Detected game start from callback")
                    
            except Exception as e:
                print(f"[NETWORK] Error receiving data: {e}")
                self.connected = False
                break