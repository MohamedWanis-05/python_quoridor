import pygame
##############
from game.board import Board
from ui.Homescreen import HomeScreen
from ui.renderer import Renderer
from game.constants import WINDOW_WIDTH, WINDOW_HEIGHT, FPS
from game.constants import TILE_SIZE
from game.rules import resolve_move, resolve_diagonal_move, check_winner

pygame.init()

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Quoridor")

clock = pygame.time.Clock()

homescreen = HomeScreen(screen)
board = Board()
renderer = Renderer(screen)

game_state = "MENU"
game_mode = None
winner = None
running = True

while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        if game_state == "MENU":
            selected_start_mode = homescreen.handle_event(event)

            if selected_start_mode is not None:
                game_mode = selected_start_mode
                game_state = "PLAYING"

        elif event.type == pygame.KEYDOWN and winner is None:
            player = board.current_player

            dr = 0
            dc = 0
            diagonal_position = None
            
            if player.player_id == 1:
                if event.key == pygame.K_UP:
                    dr = -1
                elif event.key == pygame.K_DOWN:
                    dr = 1
                elif event.key == pygame.K_LEFT:
                    dc = -1
                elif event.key == pygame.K_RIGHT:
                    dc = 1

            elif player.player_id == 2:
                if event.key == pygame.K_w:
                    dr = -1
                elif event.key == pygame.K_s:
                    dr = 1
                elif event.key == pygame.K_a:
                    dc = -1
                elif event.key == pygame.K_d:
                    dc = 1

            # =========================
            # Resolve movement
            # =========================

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


            # =========================
            # Apply movement
            # =========================

            if new_position is not None:

                board.set_player_position(
                    player.player_id,
                    new_position
                )

                winner = check_winner(board)

                if winner is None:
                    board.switch_turn()

                else:
                    print(f"Player {winner} wins!")

                    winner = check_winner(board)

                    if winner is None:
                        board.switch_turn()
                    else:
                        print(f"Player {winner} wins!")

        elif event.type == pygame.MOUSEBUTTONDOWN and winner is None:
            if event.button == 1:  # Left mouse button
                mouse_x, mouse_y = event.pos
                closest_col = round(mouse_x / TILE_SIZE)
                closest_row = round(mouse_y / TILE_SIZE)

                if 1 <= closest_col <= 8 and 1 <= closest_row <= 8:
                    wall_c = closest_col - 1
                    wall_r = closest_row - 1

                    # Check whether the mouse is closer to the horizontal line or vertical line of the intersection
                    dist_x = abs(mouse_x - closest_col * TILE_SIZE)
                    dist_y = abs(mouse_y - closest_row * TILE_SIZE)

                    is_horizontal = dist_y < dist_x

                    if board.place_wall(wall_r, wall_c, is_horizontal):
                        board.switch_turn()

    if game_state == "MENU":
        homescreen.draw()
    elif game_state == "PLAYING":
        if winner == 1:
            renderer.draw(board, p1_message="You win!")
        elif winner == 2:
            renderer.draw(board, p2_message="You win!")
        else:
            if board.current_player.player_id == 1:
                renderer.draw(board, p1_message="Your turn")
            else:
                renderer.draw(board, p2_message="Your turn")
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()