import pygame

from game.board import Board
from ui.renderer import Renderer
from game.constants import WINDOW_WIDTH, WINDOW_HEIGHT, FPS
from game.rules import resolve_move, check_winner


pygame.init()

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Quoridor")

clock = pygame.time.Clock()

board = Board()
renderer = Renderer(screen)

winner = None
running = True

while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN and winner is None:
            player_id = board.current_player

            dr = 0
            dc = 0

            if player_id == 1:
                if event.key == pygame.K_UP:
                    dr = -1
                elif event.key == pygame.K_DOWN:
                    dr = 1
                elif event.key == pygame.K_LEFT:
                    dc = -1
                elif event.key == pygame.K_RIGHT:
                    dc = 1

            elif player_id == 2:
                if event.key == pygame.K_w:
                    dr = -1
                elif event.key == pygame.K_s:
                    dr = 1
                elif event.key == pygame.K_a:
                    dc = -1
                elif event.key == pygame.K_d:
                    dc = 1

            if dr != 0 or dc != 0:
                new_position = resolve_move(board, player_id, dr, dc)

                if new_position is not None:
                    board.set_player_position(player_id, new_position)

                    winner = check_winner(board)

                    if winner is None:
                        board.switch_turn()
                    else:
                        print(f"Player {winner} wins!")

    renderer.draw(board)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()