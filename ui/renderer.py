import pygame
from game.constants import TILE_SIZE, BOARD_SIZE, WHITE, BLACK


class Renderer:
    def __init__(self, screen):
        self.screen = screen

    def draw(self, board):
        self.screen.fill(WHITE)
        self.draw_grid()
        self.draw_players(board)

    def draw_grid(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                rect = pygame.Rect(
                    col * TILE_SIZE,
                    row * TILE_SIZE,
                    TILE_SIZE,
                    TILE_SIZE
                )
                pygame.draw.rect(self.screen, BLACK, rect, 1)

    def draw_players(self, board):
        for player_id, position in board.player_positions.items():
            row, col = position
            center = (
                col * TILE_SIZE + TILE_SIZE // 2,
                row * TILE_SIZE + TILE_SIZE // 2
            )

            color = (220, 20, 60) if player_id == 1 else (30, 144, 255)
            pygame.draw.circle(self.screen, color, center, TILE_SIZE // 3)