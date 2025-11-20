import pygame
import random
from classes.constants import WIDTH, HEIGHT

# Initialisation
pygame.init()

# Polices
title_font = pygame.font.Font("assets/ps2p.ttf", 75)
button_font = pygame.font.Font("assets/ps2p.ttf", 25)
text_font = pygame.font.Font("assets/ps2p.ttf", 20)

# Couleurs
COLORS = {
    "primary": (41, 128, 185),
    "secondary": (39, 174, 96),
    "accent": (231, 76, 60),
    "text": (236, 240, 241),
    "text_dark": (44, 62, 80),
    "overlay": (0, 0, 0, 180),
    "title": (239, 191, 4),
    "background": (44, 62, 80)
}

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.is_hovered = False
        try:
            self.click_sound = pygame.mixer.Sound('assets/mouse-click-sound.mp3')
        except pygame.error:
            self.click_sound = None

    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, COLORS["text_dark"], self.rect, 2, border_radius=10)
        text_surf = button_font.render(self.text, True, COLORS["text"])
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def update_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos, mouse_click):
        if self.rect.collidepoint(mouse_pos) and mouse_click:
            if self.click_sound:
                self.click_sound.play()
            return True
        return False

class DifficultyMenu:
    def __init__(self, win):
        self.win = win
        self.buttons = [
            Button(WIDTH//2 - 150, 250, 300, 70, "YES", COLORS["secondary"], (46, 204, 113)),
            Button(WIDTH//2 - 150, 350, 300, 70, "NO", COLORS["primary"], (52, 152, 219)),
            Button(WIDTH//2 - 150, 450, 300, 70, "BACK", COLORS["accent"], (192, 57, 43))
        ]
        self.background = pygame.image.load("assets/background.jpg")
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

    def draw(self, surface):
        surface.blit(self.background, (0, 0))
        title_surf = title_font.render("Need help?", True, COLORS["title"])
        title_rect = title_surf.get_rect(midtop=(WIDTH//2, 100))
        surface.blit(title_surf, title_rect)

        beginner_desc_surf = text_font.render("", True, COLORS["text"])
        beginner_desc_rect = beginner_desc_surf.get_rect(midtop=(WIDTH//2, 300))
        surface.blit(beginner_desc_surf, beginner_desc_rect)

        master_desc_surf = text_font.render("", True, COLORS["text"])
        master_desc_rect = master_desc_surf.get_rect(midtop=(WIDTH//2, 400))
        surface.blit(master_desc_surf, master_desc_rect)

        for button in self.buttons:
            button.draw(surface)

    def run(self):
        clock = pygame.time.Clock()
        while True:
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = False
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit", False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_click = True
            
            for button in self.buttons:
                button.update_hover(mouse_pos)
                if button.is_clicked(mouse_pos, mouse_click):
                    if button.text == "YES":
                        return "beginner", True
                    elif button.text == "NO":
                        return "master", False
                    elif button.text == "BACK":
                        return "back", False
            
            self.draw(self.win)
            pygame.display.flip()
            clock.tick(60)

class AIDifficultyMenu:
    def __init__(self, win):
        self.win = win
        self.buttons = [
            Button(WIDTH//2 - 150, 250, 300, 70, "EASY", COLORS["secondary"], (46, 204, 113)),
            Button(WIDTH//2 - 150, 350, 300, 70, "MEDIUM", COLORS["primary"], (52, 152, 219)),
            Button(WIDTH//2 - 150, 450, 300, 70, "HARD", COLORS["accent"], (192, 57, 43)),
            Button(WIDTH//2 - 150, 550, 300, 70, "BACK", COLORS["text_dark"], (74, 92, 110))
        ]
        self.background = pygame.image.load("assets/background.jpg")
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

    def draw(self, surface):
        surface.blit(self.background, (0, 0))
        title_surf = title_font.render("Difficulty", True, COLORS["title"])  # Utiliser COLORS["title"]
        title_rect = title_surf.get_rect(midtop=(WIDTH//2, 100))
        surface.blit(title_surf, title_rect)

        for button in self.buttons:
            button.draw(surface)

    def run(self):
        clock = pygame.time.Clock()
        while True:
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = False
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_click = True
            
            for button in self.buttons:
                button.update_hover(mouse_pos)
                if button.is_clicked(mouse_pos, mouse_click):
                    if button.text == "EASY":
                        return "easy"
                    elif button.text == "MEDIUM":
                        return "medium"
                    elif button.text == "HARD":
                        return "hard"
                    elif button.text == "BACK":
                        return "back"
            
            self.draw(self.win)
            pygame.display.flip()
            clock.tick(60)

class GameModeMenu:
    def __init__(self, win):
        self.win = win
        self.buttons = [
            Button(WIDTH//2 - 150, 250, 300, 70, "2 PLAYERS", COLORS["primary"], (52, 152, 219)),
            Button(WIDTH//2 - 150, 350, 300, 70, "VS AI", COLORS["secondary"], (46, 204, 113)),
            Button(WIDTH//2 - 150, 450, 300, 70, "BACK", COLORS["accent"], (192, 57, 43))
        ]
        self.background = pygame.image.load("assets/background.jpg")
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        self.difficulty_menu = DifficultyMenu(win)
        self.ai_difficulty_menu = AIDifficultyMenu(win)

    def draw(self, surface):
        surface.blit(self.background, (0, 0))
        title_surf = title_font.render("LOCAL PLAY", True, COLORS["title"])
        title_rect = title_surf.get_rect(midtop=(WIDTH//2, 100))
        surface.blit(title_surf, title_rect)
        for button in self.buttons:
            button.draw(surface)

    def run(self):
        clock = pygame.time.Clock()
        while True:
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = False
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit", None, None, False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_click = True
            
            for button in self.buttons:
                button.update_hover(mouse_pos)
                if button.is_clicked(mouse_pos, mouse_click):
                    if button.text == "2 PLAYERS":
                        result = self.difficulty_menu.run()
                        if result[0] == "quit":
                            return "quit", None, None, False
                        elif result[0] == "back":
                            continue
                        return "multiplayer", result[0], None, result[1]
                    elif button.text == "VS AI":
                        result = self.difficulty_menu.run()
                        if result[0] == "quit":
                            return "quit", None, None, False
                        elif result[0] == "back":
                            continue
                        ai_difficulty = self.ai_difficulty_menu.run()
                        if ai_difficulty == "quit":
                            return "quit", None, None, False
                        elif ai_difficulty == "back":
                            continue
                        return "vsAI", result[0], ai_difficulty, result[1]
                    elif button.text == "BACK":
                        return "back", None, None, False
            
            self.draw(self.win)
            pygame.display.flip()
            clock.tick(60)

class PauseMenu:
    def __init__(self, win, background):
        self.win = win
        self.background = background
        self.box_width = 400
        self.box_height = 400
        self.box_x = WIDTH // 2 - self.box_width // 2
        self.box_y = HEIGHT // 2 - self.box_height // 2
        button_width = 300
        button_height = 70
        button_x = self.box_x + (self.box_width - button_width) // 2
        total_buttons_height = 3 * button_height + 2 * 20
        button_start_y = self.box_y + (self.box_height - total_buttons_height) // 2 + 50
        self.buttons = [
            Button(button_x, button_start_y, button_width, button_height, "RESUME", COLORS["secondary"], (46, 204, 113)),
            Button(button_x, button_start_y + button_height + 20, button_width, button_height, "MAIN MENU", COLORS["primary"], (52, 152, 219)),
            Button(button_x, button_start_y + 2 * (button_height + 20), button_width, button_height, "QUIT", COLORS["accent"], (192, 57, 43))
        ]

    def draw(self, surface):
        surface.blit(self.background, (0, 0))
        
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill(COLORS["overlay"])
        surface.blit(overlay, (0, 0))
        
        box = pygame.Rect(self.box_x, self.box_y, self.box_width, self.box_height)
        pygame.draw.rect(surface, COLORS["background"], box, border_radius=20)
        
        title_surf = title_font.render("PAUSED", True, COLORS["text"])  # Conserver COLORS["text"]
        title_rect = title_surf.get_rect(midtop=(self.box_x + self.box_width // 2, self.box_y + 20))
        surface.blit(title_surf, title_rect)

        for button in self.buttons:
            button.draw(surface)

    def run(self):
        clock = pygame.time.Clock()
        while True:
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = False
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return "resume"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_click = True
            
            for button in self.buttons:
                button.update_hover(mouse_pos)
                if button.is_clicked(mouse_pos, mouse_click):
                    if button.text == "RESUME":
                        return "resume"
                    elif button.text == "MAIN MENU":
                        return "main_menu"
                    elif button.text == "QUIT":
                        return "quit"
            
            self.draw(self.win)
            pygame.display.flip()
            clock.tick(60)

class OnlineMenu:
    def __init__(self, win):
        self.win = win
        self.background = pygame.image.load("assets/background.jpg")
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        
        # Input box for player name
        self.name_input = ""
        self.input_active = True
        self.input_box = pygame.Rect(WIDTH//2 - 200, 300, 400, 50)
        
        # Server IP input (default to localhost)
        self.server_ip = "localhost"
        self.server_ip_input_active = False
        self.server_ip_box = pygame.Rect(WIDTH//2 - 200, 400, 400, 50)
        
        # Buttons
        self.buttons = [
            Button(WIDTH//2 - 150, 500, 300, 70, "CONNECT", COLORS["secondary"], (46, 204, 113)),
            Button(WIDTH//2 - 150, 600, 300, 70, "BACK", COLORS["accent"], (192, 57, 43))
        ]
        
        # Network
        self.network = None
        self.connected = False
        self.players = {}
        self.player_id = None
        self.game_started = False
        
        # Error message
        self.error_message = ""
        self.error_timer = 0
        
        try:
            self.click_sound = pygame.mixer.Sound('assets/mouse-click-sound.mp3')
        except pygame.error:
            self.click_sound = None
    
    def handle_network_message(self, message):
        """Handle incoming network messages"""
        if message["type"] == "players_update":
            self.players = message["players"]
            self.game_started = message["game_started"]
            
            if self.game_started:
                # Game has been started by the host
                print(f"[CLIENT] Received game start signal from players_update")
                return "start_game"
        
        elif message["type"] == "game_started":
            # Direct game start notification
            print(f"[CLIENT] Received direct game start notification")
            self.game_started = True
            return "start_game"
                
        elif message["type"] == "game_state":
            # This will be handled by the game class
            pass
            
        return None
    
    def draw_waiting_room(self, surface):
        """Draw the waiting room screen"""
        surface.blit(self.background, (0, 0))
        
        title_surf = title_font.render("WAITING ROOM", True, COLORS["title"])
        title_rect = title_surf.get_rect(midtop=(WIDTH//2, 100))
        surface.blit(title_surf, title_rect)
        
        # Draw players list
        y_offset = 250
        for player_id, player_name in self.players.items():
            if player_id == 1:
                player_text = f"Player 1 (Host): {player_name}"
            else:
                player_text = f"Player {player_id}: {player_name}"
                
            text_surf = button_font.render(player_text, True, COLORS["text"])
            text_rect = text_surf.get_rect(midtop=(WIDTH//2, y_offset))
            surface.blit(text_surf, text_rect)
            y_offset += 60
        
        # Draw status message
        if len(self.players) < 2:
            status_surf = button_font.render("Waiting for another player...", True, COLORS["accent"])
            status_rect = status_surf.get_rect(midtop=(WIDTH//2, y_offset + 40))
            surface.blit(status_surf, status_rect)
        
        # Draw start game button for host only
        if self.player_id == 1 and len(self.players) == 2:
            start_button = Button(WIDTH//2 - 150, y_offset + 100, 300, 70, "START GAME", COLORS["secondary"], (46, 204, 113))
            start_button.draw(surface)
            return start_button
        
        # Draw disconnect button
        disconnect_button = Button(WIDTH//2 - 150, HEIGHT - 100, 300, 70, "DISCONNECT", COLORS["accent"], (192, 57, 43))
        disconnect_button.draw(surface)
        return disconnect_button
    
    def draw_connection_screen(self, surface):
        """Draw the connection screen"""
        surface.blit(self.background, (0, 0))
        
        title_surf = title_font.render("PLAY ONLINE", True, COLORS["title"])
        title_rect = title_surf.get_rect(midtop=(WIDTH//2, 100))
        surface.blit(title_surf, title_rect)
        
        # Draw name input prompt
        name_prompt = text_font.render("Enter your name:", True, COLORS["text"])
        name_prompt_rect = name_prompt.get_rect(midtop=(WIDTH//2, 250))
        surface.blit(name_prompt, name_prompt_rect)
        
        # Draw name input box
        pygame.draw.rect(surface, COLORS["text"] if self.input_active else COLORS["text_dark"], 
                        self.input_box, 2, border_radius=10)
        name_surf = text_font.render(self.name_input, True, COLORS["text"])
        surface.blit(name_surf, (self.input_box.x + 10, self.input_box.y + 15))
        
        # Draw server IP prompt
        server_prompt = text_font.render("Server IP (default: localhost):", True, COLORS["text"])
        server_prompt_rect = server_prompt.get_rect(midtop=(WIDTH//2, 370))
        surface.blit(server_prompt, server_prompt_rect)
        
        # Draw server IP input box
        pygame.draw.rect(surface, COLORS["text"] if self.server_ip_input_active else COLORS["text_dark"], 
                        self.server_ip_box, 2, border_radius=10)
        server_surf = text_font.render(self.server_ip, True, COLORS["text"])
        surface.blit(server_surf, (self.server_ip_box.x + 10, self.server_ip_box.y + 15))
        
        # Draw error message if any
        if self.error_message and pygame.time.get_ticks() - self.error_timer < 5000:  # Show for 5 seconds
            error_surf = text_font.render(self.error_message, True, COLORS["accent"])
            error_rect = error_surf.get_rect(midtop=(WIDTH//2, 460))
            surface.blit(error_surf, error_rect)
        
        # Draw buttons
        for button in self.buttons:
            button.draw(surface)
    
    def run(self):
        """Run the online menu loop"""
        from classes.network import Network
        
        clock = pygame.time.Clock()
        
        while True:
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = False
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.network and self.connected:
                        self.network.disconnect()
                    return "quit", None, None, True  # Always enable visual help in online mode
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_click = True
                    if not self.connected:
                        # Check input box clicks
                        if self.input_box.collidepoint(event.pos):
                            self.input_active = True
                            self.server_ip_input_active = False
                        elif self.server_ip_box.collidepoint(event.pos):
                            self.input_active = False
                            self.server_ip_input_active = True
                        else:
                            self.input_active = False
                            self.server_ip_input_active = False
                
                if event.type == pygame.KEYDOWN:
                    if self.input_active:
                        if event.key == pygame.K_RETURN:
                            self.input_active = False
                        elif event.key == pygame.K_BACKSPACE:
                            self.name_input = self.name_input[:-1]
                        else:
                            # Limit name length to 20 characters
                            if len(self.name_input) < 20:
                                self.name_input += event.unicode
                    
                    elif self.server_ip_input_active:
                        if event.key == pygame.K_RETURN:
                            self.server_ip_input_active = False
                        elif event.key == pygame.K_BACKSPACE:
                            self.server_ip = self.server_ip[:-1]
                        else:
                            # Only allow valid IP characters
                            if event.unicode.isdigit() or event.unicode == '.' or event.unicode.isalpha():
                                self.server_ip += event.unicode
            
            # Handle different screens based on connection state
            if not self.connected:
                # Draw connection screen
                self.draw_connection_screen(self.win)
                
                # Handle button clicks
                for button in self.buttons:
                    button.update_hover(mouse_pos)
                    if button.is_clicked(mouse_pos, mouse_click):
                        if button.text == "CONNECT":
                            if len(self.name_input.strip()) < 2:
                                self.error_message = "Name must be at least 2 characters"
                                self.error_timer = pygame.time.get_ticks()
                                if self.click_sound:
                                    self.click_sound.play()
                                continue
                            
                            # Attempt to connect
                            self.network = Network()
                            
                            if self.server_ip:
                                self.network.set_server(self.server_ip)
                            
                            self.network.set_callback(self.handle_network_message)
                            self.player_id = self.network.connect()
                            
                            if self.player_id is not None:
                                # Successfully connected, send name
                                if self.network.send_name(self.name_input):
                                    self.connected = True
                                else:
                                    self.error_message = "Failed to send name to server"
                                    self.error_timer = pygame.time.get_ticks()
                            else:
                                self.error_message = "Could not connect to server"
                                self.error_timer = pygame.time.get_ticks()
                                
                            if self.click_sound:
                                self.click_sound.play()
                                
                        elif button.text == "BACK":
                            return "back", None, None, True  # Always enable visual help in online mode
            else:
                # Draw waiting room
                action_button = self.draw_waiting_room(self.win)
                action_button.update_hover(mouse_pos)
                
                if action_button.is_clicked(mouse_pos, mouse_click):
                    if action_button.text == "START GAME":
                        # Host starts the game
                        if self.network.start_game():
                            print(f"[CLIENT] Player {self.player_id} starting game (responding to host command)")
                            return "online", self.name_input, self.network, True  # Always enable visual help in online mode
                    
                    elif action_button.text == "DISCONNECT":
                        self.network.disconnect()
                        self.connected = False
                        self.players = {}
                
                # Check if game was started by host
                if self.network and self.game_started:
                    print(f"[CLIENT] Player {self.player_id} starting game (responding to host command)")
                    return "online", self.name_input, self.network, True  # Always enable visual help in online mode
            
            pygame.display.flip()
            clock.tick(60)

class MainMenu:
    def __init__(self, win):
        self.win = win
        self.buttons = [
            Button(WIDTH//2 - 150, 250, 300, 70, "PLAY LOCAL", COLORS["secondary"], (46, 204, 113)),
            Button(WIDTH//2 - 150, 350, 300, 70, "PLAY ONLINE", COLORS["primary"], (52, 152, 219)),
            Button(WIDTH//2 - 150, 450, 300, 70, "ABOUT", COLORS["primary"], (52, 152, 219)),
            Button(WIDTH//2 - 150, 550, 300, 70, "EXIT", COLORS["accent"], (192, 57, 43))
        ]
        self.game_mode_menu = GameModeMenu(win)
        self.online_menu = OnlineMenu(win)
        self.show_about = False
        self.about_text = [
            "Developed by:",
            "Mohammed Yassine Habchi",
            "Mohamed Walid Kharmoudi",
            "Amine Izmaoun",
            "Anass Chadli",
            "Mohamed Zaari",
            "Youssef Boulafra",
            "Mohamed Aymane Bouhmouch"
        ]
        self.background = pygame.image.load("assets/background.jpg")
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

    def draw_about(self, surface):
        surface.blit(self.background, (0, 0))
        
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill(COLORS["overlay"])
        surface.blit(overlay, (0, 0))
        
        box_height = 500
        box = pygame.Rect(WIDTH//2 - 250, HEIGHT//2 - box_height//2, 500, box_height)
        pygame.draw.rect(surface, COLORS["background"], box, border_radius=20)
        
        title_surf = title_font.render("ABOUT", True, COLORS["text"])
        title_rect = title_surf.get_rect(midtop=(WIDTH//2, HEIGHT//2 - box_height//2 + 30))
        surface.blit(title_surf, title_rect)
        
        start_y = HEIGHT//2 - box_height//2 + 120
        line_height = 40
        
        for i, line in enumerate(self.about_text):
            if line:
                text_surf = text_font.render(line, True, COLORS["text"])
                text_rect = text_surf.get_rect(midtop=(WIDTH//2, start_y + i * line_height))
                surface.blit(text_surf, text_rect)
        
        back_button = Button(WIDTH//2 - 75, HEIGHT//2 + box_height//4 + 80, 150, 50, "BACK", COLORS["accent"], (192, 57, 43))
        back_button.draw(surface)
        return back_button

    def draw(self, surface):
        surface.blit(self.background, (0, 0))
        
        if self.show_about:
            back_button = self.draw_about(surface)
            return back_button
        else:
            title_surf = title_font.render("CHECKERS", True, COLORS["title"])
            title_rect = title_surf.get_rect(midtop=(WIDTH//2, 100))
            surface.blit(title_surf, title_rect)

            for button in self.buttons:
                button.draw(surface)
            return None

    def run(self):
        clock = pygame.time.Clock()
        while True:
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = False
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return "quit", None, None, False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_click = True
            
            if self.show_about:
                back_button = self.draw(self.win)
                back_button.update_hover(mouse_pos)
                if back_button.is_clicked(mouse_pos, mouse_click):
                    self.show_about = False
            else:
                for button in self.buttons:
                    button.update_hover(mouse_pos)
                    if button.is_clicked(mouse_pos, mouse_click):
                        if button.text == "PLAY LOCAL":
                            mode, player_difficulty, ai_difficulty, show_help = self.game_mode_menu.run()
                            if mode in ["multiplayer", "vsAI"]:
                                return mode, player_difficulty, ai_difficulty, show_help
                            elif mode == "quit":
                                pygame.quit()
                                return "quit", None, None, False
                        elif button.text == "PLAY ONLINE":
                            result = self.online_menu.run()
                            if len(result) == 4:  # Check if we got all 4 values
                                mode, player_name, network, show_help = result
                                if mode == "online":
                                    return mode, player_name, network, show_help
                                elif mode == "quit":
                                    pygame.quit()
                                    return "quit", None, None, False
                            else:
                                # Handle case where we don't get all 4 values
                                print("Warning: Unexpected return value from online menu")
                                return "quit", None, None, False
                        elif button.text == "ABOUT":
                            self.show_about = True
                        elif button.text == "EXIT":
                            pygame.quit()
                            return "quit", None, None, False
            
            self.draw(self.win)
            pygame.display.flip()
            clock.tick(60)