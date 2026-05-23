import pygame
from ai.easy_ai import get_easy_ai_move
from ai.medium_ai import get_medium_ai_move
from ai.hard_ai import get_hard_ai_move
##############
from game.board import Board
from ui.Homescreen import HomeScreen
from ui.renderer import Renderer
from game.constants import WINDOW_WIDTH, WINDOW_HEIGHT, FPS
from game.constants import TILE_SIZE
from game.rules import resolve_move, resolve_diagonal_move, check_winner

pygame.init()
board = Board()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Quoridor")

clock = pygame.time.Clock()

homescreen = HomeScreen(screen)
renderer = Renderer(screen)

game_state = "MENU"
game_mode = None
ai_difficulty = "Easy"
board_size = 9
winner = None
running = True
move_flags = None  # -100 for wall block, -200 for out of board
hovered_wall = None

def get_valid_highlights(board):
    """Return all valid moves and their corresponding keys for the current player."""
    player_id = board.current_player.player_id
    row, col = board.get_player_position(player_id)

    valid_moves = []

    if player_id == 1:
        dir_keys = {(-1, 0): "UP", (1, 0): "DOWN", (0, -1): "LEFT", (0, 1): "RIGHT"}
        diag_keys = {
            (row - 1, col - 1): "U", (row - 1, col + 1): "O",
            (row + 1, col - 1): "J", (row + 1, col + 1): "L"
        }
    else:
        dir_keys = {(-1, 0): "W", (1, 0): "S", (0, -1): "A", (0, 1): "D"}
        diag_keys = {
            (row - 1, col - 1): "Q", (row - 1, col + 1): "E",
            (row + 1, col - 1): "Z", (row + 1, col + 1): "C"
        }
    for (dr, dc), key_name in dir_keys.items():
        move = resolve_move(board, player_id, dr, dc)
        if move not in {None, -100, -200}:
            valid_moves.append((move, key_name))

    for position, key_name in diag_keys.items():
        move = resolve_diagonal_move(board, player_id, position)
        if move not in {None, -100, -200}:
            valid_moves.append((move, key_name))

    return valid_moves


while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if game_state == "MENU":
            selected_start_mode = homescreen.handle_event(event)

            if selected_start_mode is not None:
                game_mode = selected_start_mode["mode"]
                board_size = selected_start_mode["size"]
                game_state = "PLAYING"
                screen = pygame.display.set_mode((board.size * TILE_SIZE + 200, board.size * TILE_SIZE + 100))
                renderer.screen = screen
                board = Board(size=board_size)

        elif event.type == pygame.KEYDOWN and winner is None:
            if game_mode == "1vAI" and board.current_player.player_id == 2:
                continue

            player = board.current_player

            dr = 0
            dc = 0
            diagonal_position = None

            row, col = board.get_player_position(player.player_id)

            if player.player_id == 1:
                # Orthogonal keys
                if event.key == pygame.K_UP:
                    dr = -1
                elif event.key == pygame.K_DOWN:
                    dr = 1
                elif event.key == pygame.K_LEFT:
                    dc = -1
                elif event.key == pygame.K_RIGHT:
                    dc = 1
                elif event.key == pygame.K_u:
                    diagonal_position = (row - 1, col - 1)
                elif event.key == pygame.K_o:
                    diagonal_position = (row - 1, col + 1)
                elif event.key == pygame.K_j:
                    diagonal_position = (row + 1, col - 1)
                elif event.key == pygame.K_l:
                    diagonal_position = (row + 1, col + 1)

            elif player.player_id == 2:

                if event.key == pygame.K_w:
                    dr = -1
                elif event.key == pygame.K_s:
                    dr = 1
                elif event.key == pygame.K_a:
                    dc = -1
                elif event.key == pygame.K_d:
                    dc = 1

                elif event.key == pygame.K_q:
                    diagonal_position = (row - 1, col - 1)
                elif event.key == pygame.K_e:
                    diagonal_position = (row - 1, col + 1)
                elif event.key == pygame.K_z:
                    diagonal_position = (row + 1, col - 1)
                elif event.key == pygame.K_c:
                    diagonal_position = (row + 1, col + 1)

            if diagonal_position is not None:
                new_position = resolve_diagonal_move(
                    board,
                    player.player_id,
                    diagonal_position
                )

            elif dr != 0 or dc != 0:
                new_position = resolve_move(
                    board,
                    player.player_id,
                    dr,
                    dc
                )
            else:
                new_position = None
            move_flags = new_position
            if new_position not in {None, -100, -200}:
                board.set_player_position(
                    player.player_id,
                    new_position
                )
                winner = check_winner(board)
                if winner is None:
                    board.switch_turn()
                else:
                    print(f"Player {winner} wins!")

        elif event.type == pygame.MOUSEBUTTONDOWN and game_state == "PLAYING":
            if event.button == 1:
                mouse_x, mouse_y = event.pos

                if renderer.btn_menu.collidepoint(mouse_x, mouse_y):
                    game_state = "MENU"
                    board = Board()
                    winner = None
                    screen = pygame.display.set_mode((800, 800))
                    homescreen.screen = screen
                    continue

                elif renderer.btn_reset.collidepoint(mouse_x, mouse_y):
                    board = Board(size=board_size)
                    winner = None
                    continue

                if winner is None:
                    if game_mode == "1vAI" and board.current_player.player_id == 2:
                        continue

                    closest_col = round(mouse_x / TILE_SIZE)
                    closest_row = round(mouse_y / TILE_SIZE)

                    if 1 <= closest_col <= board.size - 1 and 1 <= closest_row <= board.size - 1:
                        wall_c = closest_col - 1
                        wall_r = closest_row - 1

                        dist_x = abs(mouse_x - closest_col * TILE_SIZE)
                        dist_y = abs(mouse_y - closest_row * TILE_SIZE)
                        is_horizontal = dist_y < dist_x

                        if board.place_wall(wall_r, wall_c, is_horizontal):
                            board.switch_turn()

        if game_state == "PLAYING" and winner is None:
            hovered_wall = None
            valid_moves = []

            if game_mode == "1vAI" and board.current_player.player_id == 2:
                ai_move = None
                # Temporarily draw to show "Thinking..."
                renderer.draw(board, p2_message="Thinking...", hovered_wall=None, valid_moves=[])
                pygame.display.flip()
                pygame.time.delay(400)

                if ai_difficulty == "Easy":
                    ai_move = get_easy_ai_move(board)
                elif ai_difficulty == "Medium":
                    ai_move = get_medium_ai_move(board)
                elif ai_difficulty == "Hard":
                    ai_move = get_hard_ai_move(board)

                if ai_move is not None:
                    if ai_move["type"] == "pawn_move":
                        board.set_player_position(2, ai_move["position"])
                        move_flags = None
                        winner = check_winner(board)
                        if winner is None:
                            board.switch_turn()
                        else:
                            print(f"Player {winner} wins!")
                    elif ai_move["type"] == "place_wall":
                        if board.place_wall(ai_move["row"], ai_move["col"], ai_move["is_horizontal"]):
                            move_flags = None
                            board.switch_turn()
            else:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                closest_col = round(mouse_x / TILE_SIZE)
                closest_row = round(mouse_y / TILE_SIZE)

                if 1 <= closest_col <= board.size - 1 and 1 <= closest_row <= board.size - 1:
                    wall_c = closest_col - 1
                    wall_r = closest_row - 1
                    dist_x = abs(mouse_x - closest_col * TILE_SIZE)
                    dist_y = abs(mouse_y - closest_row * TILE_SIZE)
                    is_horizontal = dist_y < dist_x

                    if (wall_r, wall_c) not in board.horizontal_walls and (wall_r, wall_c) not in board.vertical_walls:
                        hovered_wall = (wall_r, wall_c, is_horizontal)
                valid_moves = get_valid_highlights(board)

    # ==========================================
    # RENDERING
    # ==========================================
    if game_state == "MENU":
        homescreen.draw()
    elif game_state == "PLAYING":

        moves_to_draw = valid_moves if 'valid_moves' in locals() else []

        if winner == 1:
            renderer.draw(board, p1_message="You win!", p1_message_color=(0, 255, 0), valid_moves=[])
        elif winner == 2:
            renderer.draw(board, p2_message="You win!", p2_message_color=(0, 255, 0), valid_moves=[])
        elif move_flags == -100 and board.current_player.player_id == 1:
            renderer.draw(board, p1_message="Wall block", p1_message_color=(255, 0, 0), hovered_wall=hovered_wall,
                          valid_moves=moves_to_draw)
        elif move_flags == -100 and board.current_player.player_id == 2:
            renderer.draw(board, p2_message="Wall block", p2_message_color=(255, 0, 0), hovered_wall=hovered_wall,
                          valid_moves=moves_to_draw)
        elif move_flags == -200 and board.current_player.player_id == 1:
            renderer.draw(board, p1_message="Outside of Board", p1_message_color=(255, 0, 0), hovered_wall=hovered_wall,
                          valid_moves=moves_to_draw)
        elif move_flags == -200 and board.current_player.player_id == 2:
            renderer.draw(board, p2_message="Outside of Board", p2_message_color=(255, 0, 0), hovered_wall=hovered_wall,
                          valid_moves=moves_to_draw)
        else:
            if board.current_player.player_id == 1:
                renderer.draw(board, p1_message="Your turn", hovered_wall=hovered_wall, valid_moves=moves_to_draw)
            else:
                renderer.draw(board, p2_message="Your turn", hovered_wall=hovered_wall, valid_moves=moves_to_draw)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()