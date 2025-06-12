import pygame
from board import Board
from pieces import pawn
from constants import WIDTH, HEIGHT, SQUARE_SIZE, BOARD_HEIGHT, UI_HEIGHT



music_on = True



def show_menu():
    menu_running = True
    global music_on

    # Load background and button images
    bg_image = pygame.image.load("assets/menu_background.jpg")
    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT + UI_HEIGHT))

    start_img = pygame.transform.scale(pygame.image.load("assets/start_button.png"), (170, 60))
    start_hover_img = pygame.transform.scale(pygame.image.load("assets/start_button_hover.png"), (170, 60))
    exit_img = pygame.transform.scale(pygame.image.load("assets/exit_button.png"), (170, 60))
    exit_hover_img = pygame.transform.scale(pygame.image.load("assets/exit_button_hover.png"), (170, 60))

    start_rect = start_img.get_rect(center=(WIDTH // 2, 500))
    exit_rect = exit_img.get_rect(center=(WIDTH // 2, 600))

    music_on_img = pygame.transform.scale(pygame.image.load("assets/music_on.png"), (120, 120))
    music_off_img = pygame.transform.scale(pygame.image.load("assets/music_off.png"), (120, 120))
    music_btn_rect = music_on_img.get_rect(topleft=(WIDTH - 120, 4))
    

    # sound effects
    click_sound = pygame.mixer.Sound("assets/click.wav")
    click_sound.set_volume(0.5)
    pygame.mixer.music.load("assets/menu_music.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)


    # Fonts
    title_font = pygame.font.SysFont("georgia", 72, bold=True)

    while menu_running:
        WIN.blit(bg_image, (0, 0))

        # Draw title
        title_surface = title_font.render("CHESS", True, (0, 0, 0))
        WIN.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 100))

        # Blit button images
        mx, my = pygame.mouse.get_pos()

        if start_rect.collidepoint(mx, my):
            WIN.blit(start_hover_img, start_rect)
        else:
            WIN.blit(start_img, start_rect)

        if exit_rect.collidepoint(mx, my):
            WIN.blit(exit_hover_img, exit_rect)
        else:
            WIN.blit(exit_img, exit_rect)


        WIN.blit(music_on_img if music_on else music_off_img, music_btn_rect)


        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                click_sound.play()
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if start_rect.collidepoint(mx, my):
                    click_sound.play()
                    menu_running = False
                elif exit_rect.collidepoint(mx, my):
                    click_sound.play()
                    pygame.quit()
                    exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                if music_btn_rect.collidepoint(mx, my):
                    music_on = not music_on
                    if music_on:
                        pygame.mixer.music.unpause()
                    else:
                        pygame.mixer.music.pause()


# Initialize Pygame
pygame.init()
WIN = pygame.display.set_mode((WIDTH, BOARD_HEIGHT + UI_HEIGHT))
pygame.display.set_caption("CHESS")

show_menu()

# Game variables
board = Board()
selected_piece = None
valid_moves = []
turn = 'white'
promoting = False
promotion_pos = None
options = []
game_over = False
winner = None
in_check_player = None

music_on_img = pygame.transform.scale(pygame.image.load("assets/music_on.png"), (120, 120))
music_off_img = pygame.transform.scale(pygame.image.load("assets/music_off.png"), (120, 120))
music_btn_rect = music_on_img.get_rect(bottomright=(WIDTH - 0.005, 740))

font = pygame.font.SysFont("arial", 24)

# main game loop
running = True
while running:
    WIN.fill((0, 0, 0))
    board.draw(WIN, selected=selected_piece, valid_moves=valid_moves)

    #music_btn_rect = pygame.Rect(WIDTH - 60, 10, 40, 40)
    WIN.blit(music_on_img if music_on else music_off_img, music_btn_rect)


    # Show check message
    if in_check_player and not game_over:
        msg = font.render(f"{in_check_player.capitalize()} is in check!", True, (255, 0, 0))
        WIN.blit(msg, (10, BOARD_HEIGHT + 20))

    # Show game over
    if game_over and winner:
        msg = font.render(f"{winner.capitalize()} wins by checkmate!", True, (255, 0, 0))
        WIN.blit(msg, (WIDTH // 2 - msg.get_width() // 2, BOARD_HEIGHT + 20))

    # Show promotion options
    if promoting:
        pygame.draw.rect(WIN, (200, 200, 200), (0, BOARD_HEIGHT, WIDTH, UI_HEIGHT))
        for i, option in enumerate(options):
            if option.image:
                WIN.blit(option.image, (i * 60, BOARD_HEIGHT + 10))
                pygame.draw.rect(WIN, (0, 0, 0), (i * 60, BOARD_HEIGHT + 10, 60, 60), 2)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            pos = pygame.mouse.get_pos()

            if music_btn_rect.collidepoint(pos):
                music_on = not music_on
                if music_on:
                    pygame.mixer.music.play(-1)
                else:
                    pygame.mixer.music.stop()
                continue  # Prevent other piece logic from firing


            if promoting:
                mx, my = pos
                for i, option in enumerate(options):
                    rect = pygame.Rect(i * 60, BOARD_HEIGHT + 10, 60, 60)
                    if rect.collidepoint(mx, my):
                        r, c = promotion_pos
                        board.board[r][c] = type(option)(turn, r, c)

                        for j, captured in enumerate(board.captured_pieces[turn]):
                            if type(captured) == type(option):
                                del board.captured_pieces[turn][j]
                                break

                        promoting = False
                        promotion_pos = None

                        # Check/checkmate after promotion
                        opponent = 'black' if turn == 'white' else 'white'
                        if board.is_checkmate(opponent):
                            game_over = True
                            winner = turn
                        elif board.is_in_check(opponent):
                            in_check_player = opponent
                        else:
                            in_check_player = None

                        turn = opponent
                        selected_piece = None
                        valid_moves = []
                        break
                continue

            row = pos[1] // SQUARE_SIZE
            col = pos[0] // SQUARE_SIZE

            if 0 <= row < 8 and 0 <= col < 8:
                if selected_piece:
                    piece = board.board[selected_piece[0]][selected_piece[1]]
                    if piece and piece.color == turn and (row, col) in piece.get_valid_moves(board.board):
                        result, promotion_pos = board.move_piece(selected_piece, (row, col))

                        if result == 'promote':
                            captured = board.captured_pieces[turn]
                            options = [type(p)(turn, 0, 0) for p in captured if not isinstance(p, pawn)]
                            promoting = True
                        else:
                            opponent = 'black' if turn == 'white' else 'white'
                            if board.is_checkmate(opponent):
                                game_over = True
                                winner = turn
                            elif board.is_in_check(opponent):
                                in_check_player = opponent
                            else:
                                in_check_player = None
                            turn = opponent

                        selected_piece = None
                        valid_moves = []
                    else:
                        selected_piece = None
                        valid_moves = []
                else:
                    piece = board.board[row][col]
                    if piece and piece.color == turn:
                        selected_piece = (row, col)
                        valid_moves = board.filter_moves(piece, piece.get_valid_moves(board.board))  # ✅ New line
