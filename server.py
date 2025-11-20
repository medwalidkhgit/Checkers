import socket
import threading
import pickle
import time
import sys
from classes.constants import PIECE_DARK

class CheckersServer:
    def __init__(self, host='0.0.0.0', port=5555):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(2)
        
        self.clients = {}
        self.players = {}
        self.game_state = {
            "board": None,
            "turn": PIECE_DARK,  # Initialize with black's turn
            "started": False,
            "black_score": 0,  # Initialize scores
            "white_score": 0
        }
        self.player_count = 0
        self.max_players = 2
        
        print(f"[SERVER] Server started on {host}:{port}")
        
    def handle_client(self, conn, addr, player_id):
        print(f"[SERVER] New connection from {addr}, assigned player_id: {player_id}")
        
        try:
            # Send player ID to client
            conn.send(str(player_id).encode())
            
            # Wait for player name
            name = conn.recv(1024).decode()
            self.players[player_id] = {"name": name, "conn": conn, "addr": addr}
            
            print(f"[SERVER] Player {player_id} registered as '{name}'")
            
            # Tell all clients about the players
            self.broadcast_players()
            
            while True:
                try:
                    data = conn.recv(4096)
                    if not data:
                        break
                    
                    message = pickle.loads(data)
                    print(f"[SERVER] Received message type: {message['type']} from player {player_id}")
                    
                    # Handle different message types
                    if message["type"] == "start_game":
                        print(f"[SERVER] Player {player_id} started the game")
                        self.game_state["started"] = True
                        # Initialize with default turn (black's turn)
                        self.game_state["turn"] = PIECE_DARK
                        # Broadcast to all clients that the game has started
                        self.broadcast_game_started()
                    
                    elif message["type"] == "move":
                        # Update game state with the move
                        print(f"[SERVER] Received move from player {player_id}")
                        self.game_state["board"] = message["board"]
                        self.game_state["turn"] = message["turn"]
                        # Update scores from board state
                        self.game_state["black_score"] = message["board"].get("black_score", 0)
                        self.game_state["white_score"] = message["board"].get("white_score", 0)
                        self.broadcast_game_state()
                    
                except Exception as e:
                    print(f"[SERVER] Error receiving data from {addr}: {e}")
                    break
        
        except Exception as e:
            print(f"[SERVER] Error handling client {addr}: {e}")
        finally:
            print(f"[SERVER] Connection from {addr} closed")
            if player_id in self.players:
                del self.players[player_id]
                self.broadcast_players()
            
            self.player_count -= 1
            conn.close()
    
    def broadcast_players(self):
        """Send the current players list to all connected clients"""
        players_info = {}
        for pid, player in self.players.items():
            players_info[pid] = player["name"]
        
        message = {
            "type": "players_update",
            "players": players_info,
            "game_started": self.game_state["started"]
        }
        
        data = pickle.dumps(message)
        print(f"[SERVER] Broadcasting players update: {players_info}, game_started: {self.game_state['started']}")
        for player in self.players.values():
            try:
                player["conn"].send(data)
            except Exception as e:
                print(f"[SERVER] Error sending player update to {player['addr']}: {e}")
    
    def broadcast_game_started(self):
        """Send a game start notification to all clients"""
        message = {
            "type": "game_started",
            "started": True
        }
        
        data = pickle.dumps(message)
        print(f"[SERVER] Broadcasting game start notification")
        for player in self.players.values():
            try:
                player["conn"].send(data)
            except Exception as e:
                print(f"[SERVER] Error sending game start notification to {player['addr']}: {e}")
    
    def broadcast_game_state(self):
        """Send the current game state to all connected clients"""
        message = {
            "type": "game_state",
            "board": self.game_state["board"],
            "turn": self.game_state["turn"],
            "started": self.game_state["started"],
            "black_score": self.game_state["black_score"],
            "white_score": self.game_state["white_score"]
        }
        
        data = pickle.dumps(message)
        print(f"[SERVER] Broadcasting game state update. Turn: {self.game_state['turn']}, Scores: Black={self.game_state['black_score']}, White={self.game_state['white_score']}")
        for player in self.players.values():
            try:
                player["conn"].send(data)
            except Exception as e:
                print(f"[SERVER] Error sending game state to {player['addr']}: {e}")
    
    def start(self):
        print("[SERVER] Waiting for connections...")
        
        try:
            while True:
                conn, addr = self.server.accept()
                
                if self.player_count >= self.max_players:
                    print(f"[SERVER] Rejected connection from {addr}: Server full")
                    conn.send("SERVER_FULL".encode())
                    conn.close()
                    continue
                
                self.player_count += 1
                player_id = self.player_count
                
                # Start a new thread to handle this client
                thread = threading.Thread(target=self.handle_client, args=(conn, addr, player_id))
                thread.daemon = True
                thread.start()
                
        except KeyboardInterrupt:
            print("[SERVER] Server shutting down...")
        except Exception as e:
            print(f"[SERVER] An error occurred: {e}")
        finally:
            self.server.close()
            print("[SERVER] Server closed")

if __name__ == "__main__":
    server = CheckersServer()
    server.start()