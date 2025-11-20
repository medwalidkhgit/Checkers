import pygame
from classes.constants import WIDTH, HEIGHT, SQUARE_SIZE, PIECE_LIGHT, PIECE_DARK, ROWS, COLS
from classes.game import Game
from classes.menu import MainMenu, PauseMenu
from classes.ai import AIPlayer

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

# Initialisation du mixer pour le son
pygame.mixer.init()
# Chargement du fichier de son
ERROR_SOUND = pygame.mixer.Sound('assets/error.mp3')  # Assure-toi que le fichier est au bon chemin

def get_row_col_from_mouse(pos):
    board_offset_x = (WIDTH - (COLS * SQUARE_SIZE)) // 2
    board_offset_y = (HEIGHT - (ROWS * SQUARE_SIZE)) // 2
    x, y = pos
    x_adjusted = x - board_offset_x
    y_adjusted = y - board_offset_y
    row = y_adjusted // SQUARE_SIZE
    col = x_adjusted // SQUARE_SIZE
    return row, col

def draw_text_with_background(text, font, text_color, background_color, surface, x, y, width, height):
    pygame.draw.rect(surface, background_color, (x, y, width, height), border_radius=15)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    surface.blit(text_surface, text_rect)

def main():
    pygame.init()
    # Charger l'image de fond pour le menu de pause
    background = pygame.image.load("assets/background.jpg")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    
    run = True
    clock = pygame.time.Clock()
    font = pygame.font.Font("assets/ps2p.ttf", 48)
    main_menu = MainMenu(WIN)
    mode, player_difficulty, ai_difficulty, show_help = main_menu.run()  # Get help choice
    
    if mode == "quit":
        pygame.quit()
        return
    
    game = Game(WIN, player_difficulty, show_help)  # Pass help choice to Game
    # Let Game class handle show_valid_moves based on help choice
    
    ai_player = None
    network = None
    
    if mode == "vsAI":
        ai_player = AIPlayer(PIECE_LIGHT, ai_difficulty)
        # In vsAI, player controls PIECE_DARK, so enable move sound
        game.enable_move_sound = True
    elif mode == "online":
        network = ai_difficulty  # In online mode, this contains the network object
        player_name = player_difficulty  # In online mode, this contains player name
        # Use "master" as default difficulty for online mode to avoid invalid difficulty
        game = Game(WIN, "master", show_help)  # Pass help choice here too
        # Enable move sound only for player's turn
        game.enable_move_sound = False  # Will be set dynamically in event loop
        
        # Set up network callback
        def handle_network_message(message):
            nonlocal game
            
            if message["type"] == "game_state":
                # Update game state from server
                print(f"[CLIENT] Received game state update")
                if message["board"] is not None:
                    game.board.set_board_state(message["board"])
                    print(f"[CLIENT] Updated board state")
                if message["turn"] is not None:
                    game.turn = message["turn"]
                    print(f"[CLIENT] Updated turn to: {'Red' if game.turn == PIECE_LIGHT else 'Black'}")
                # Update scores
                game.black_score = message.get("black_score", game.black_score)
                game.white_score = message.get("white_score", game.white_score)
                print(f"[CLIENT] Updated scores: Black={game.black_score}, White={game.white_score}")
                game.update()
            
            elif message["type"] == "game_started":
                print(f"[CLIENT] Game started notification received in main")
                # No need to do anything here, the menu already handled this
                pass
                
            return None  # No special return value needed in main
        
        network.set_callback(handle_network_message)
        
        # For player 1 (host), send initial board state after starting
        if network.player_id == 1:
            # Wait a moment to ensure both players are ready
            pygame.time.delay(500)
            # Send initial board state
            initial_board_state = game.board.get_board_state()
            network.send_move(initial_board_state, game.turn)
            print(f"[CLIENT] Player 1 sent initial board state")
    else:
        # In multiplayer, both players are human, so enable move sound
        game.enable_move_sound = True
    
    ai_thinking = False
    ai_move_time = 0
    
    while run:
        clock.tick(60)
        
        if mode == "vsAI" and game.turn == PIECE_LIGHT and not ai_thinking:
            ai_thinking = True
            ai_move_time = pygame.time.get_ticks()
        
        if ai_thinking and pygame.time.get_ticks() - ai_move_time > 300:
            ai_player.make_move(game)
            ai_thinking = False

        winner = game.winner()
        if winner is not None:
            winner_text = f"Winner: {'White' if winner == PIECE_LIGHT else 'Black'}"
            draw_text_with_background(winner_text, font, (255, 255, 255), (50, 50, 50), WIN, WIDTH // 4, 80, WIDTH // 2, 80)
            pygame.display.update()
            pygame.time.delay(3000)
            main_menu = MainMenu(WIN)
            mode, player_difficulty, ai_difficulty, show_help = main_menu.run()  # Récupérer mode, player_difficulty, ai_difficulty, show_help
            if mode == "quit":
                run = False
            else:
                game = Game(WIN, player_difficulty, show_help)  # Passer player_difficulty et show_help à Game
                # Let Game class handle show_valid_moves based on difficulty
                if mode == "vsAI":
                    ai_player = AIPlayer(PIECE_LIGHT, ai_difficulty)
                    game.enable_move_sound = True
                elif mode == "online":
                    network = ai_difficulty
                    player_name = player_difficulty
                    game = Game(WIN, "master", show_help)
                    game.enable_move_sound = False
                    
                    # Set up network callback
                    def handle_network_message(message):
                        if message["type"] == "game_state":
                            # Update game state from server
                            if message["board"] is not None:
                                game.board.set_board_state(message["board"])
                            if message["turn"] is not None:
                                game.turn = message["turn"]
                            # Update scores
                            game.black_score = message.get("black_score", game.black_score)
                            game.white_score = message.get("white_score", game.white_score)
                            game.update()
                    
                    network.set_callback(handle_network_message)
                else:
                    ai_player = None
                    game.enable_move_sound = True
            continue

        turn_text = f"Turn: {'Red' if game.turn == PIECE_LIGHT else 'Black'}"
        draw_text_with_background(turn_text, font, (255, 255, 255), (50, 50, 50), WIN, WIDTH // 4, 10, WIDTH // 2, 60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                if network:
                    network.disconnect()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game.toggle_pause()  # Toggle pause state
                    pause_menu = PauseMenu(WIN, background)
                    pause_result = pause_menu.run()
                    if pause_result == "quit":
                        if network:
                            network.disconnect()
                        run = False
                    elif pause_result == "main_menu":
                        if network:
                            network.disconnect()
                        main_menu = MainMenu(WIN)
                        mode, player_difficulty, ai_difficulty, show_help = main_menu.run()
                        if mode == "quit":
                            run = False
                        else:
                            game = Game(WIN, player_difficulty, show_help)
                            # Let Game class handle show_valid_moves based on difficulty
                            if mode == "vsAI":
                                ai_player = AIPlayer(PIECE_LIGHT, ai_difficulty)
                                game.enable_move_sound = True
                            elif mode == "online":
                                network = ai_difficulty
                                player_name = player_difficulty
                                game = Game(WIN, "master", show_help)
                                game.enable_move_sound = False
                                
                                # Set up network callback
                                def handle_network_message(message):
                                    if message["type"] == "game_state":
                                        # Update game state from server
                                        if message["board"] is not None:
                                            game.board.set_board_state(message["board"])
                                        if message["turn"] is not None:
                                            game.turn = message["turn"]
                                        # Update scores
                                        game.black_score = message.get("black_score", game.black_score)
                                        game.white_score = message.get("white_score", game.white_score)
                                        game.update()
                                
                                network.set_callback(handle_network_message)
                            else:
                                ai_player = None
                                game.enable_move_sound = True
                    else:  # Resume game
                        game.toggle_pause()  # Toggle pause state back
                    continue
                
                # Toggle valid moves display with 'V' key
                elif event.key == pygame.K_v:
                    game.show_valid_moves = not game.show_valid_moves
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                
                # Check for pause button click
                if game.is_pause_button_clicked(pos):
                    game.toggle_pause()  # Toggle pause state
                    pause_menu = PauseMenu(WIN, background)
                    pause_result = pause_menu.run()
                    if pause_result == "quit":
                        if network:
                            network.disconnect()
                        run = False
                    elif pause_result == "main_menu":
                        if network:
                            network.disconnect()
                        main_menu = MainMenu(WIN)
                        mode, player_difficulty, ai_difficulty, show_help = main_menu.run()
                        if mode == "quit":
                            run = False
                        else:
                            game = Game(WIN, player_difficulty, show_help)
                            # Let Game class handle show_valid_moves based on difficulty
                            if mode == "vsAI":
                                ai_player = AIPlayer(PIECE_LIGHT, ai_difficulty)
                                game.enable_move_sound = True
                            elif mode == "online":
                                network = ai_difficulty
                                player_name = player_difficulty
                                game = Game(WIN, "master", show_help)
                                game.enable_move_sound = False
                                
                                # Set up network callback
                                def handle_network_message(message):
                                    if message["type"] == "game_state":
                                        # Update game state from server
                                        if message["board"] is not None:
                                            game.board.set_board_state(message["board"])
                                        if message["turn"] is not None:
                                            game.turn = message["turn"]
                                        # Update scores
                                        game.black_score = message.get("black_score", game.black_score)
                                        game.white_score = message.get("white_score", game.white_score)
                                        game.update()
                                
                                network.set_callback(handle_network_message)
                            else:
                                ai_player = None
                                game.enable_move_sound = True
                    else:  # Resume game
                        game.toggle_pause()  # Toggle pause state back
                    continue

                can_play = False
                if mode == "multiplayer":
                    can_play = True
                elif mode == "vsAI":
                    can_play = (game.turn == PIECE_DARK)
                elif mode == "online":
                    # In online mode, player 1 controls light pieces, player 2 controls dark pieces
                    player_id = network.player_id
                    if (player_id == 1 and game.turn == PIECE_LIGHT) or (player_id == 2 and game.turn == PIECE_DARK):
                        can_play = True
                        game.enable_move_sound = True
                    else:
                        game.enable_move_sound = False
                
                if can_play:
                    row, col = get_row_col_from_mouse(pos)
                    if 0 <= row < 8 and 0 <= col < 8:
                        result = game.select(row, col)
                        if result == "invalid_move" or result == "nothing_selected":
                            ERROR_SOUND.play()
                        elif result == "move_made" and mode == "online":
                            # Send move to server
                            print(f"[CLIENT] Sending move. Turn changing to: {'Red' if game.turn == PIECE_LIGHT else 'Black'}")
                            network.send_move(game.board.get_board_state(), game.turn)

        game.update()
    
    pygame.quit()

if __name__ == "__main__":
    main()