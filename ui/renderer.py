import pygame
from game.constants import TILE_SIZE, BOARD_SIZE, WHITE, BLACK, WALL_THICKNESS, WALL_COLOR


class Renderer:
    def __init__(self, screen):
        self.screen = screen
        pygame.font.init()
        self.font = pygame.font.SysFont(None, int(TILE_SIZE * 0.5))

        self.msg_font = pygame.font.SysFont(None, 28)
        self.title_font = pygame.font.SysFont(None, 32)

    def draw(self, board,p1_message="", p2_message=""):
        self.screen.fill(WHITE)
        self.draw_grid()
        self.draw_players(board)
        self.draw_walls(board)
        self.draw_side_panel(board,p1_message, p2_message)

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
            if player_id == board.current_player.player_id:
                ring_radius = (TILE_SIZE // 3) + 5
                pygame.draw.circle(self.screen, (255, 215, 0), center, ring_radius, 4)
            pygame.draw.circle(self.screen, color, center, TILE_SIZE // 3)

            if player_id == 1:
                walls_left = board.player_1.walls_remaining
            else:
                walls_left = board.player_2.walls_remaining

            text_surface = self.font.render(str(walls_left), True, WHITE)
            text_rect = text_surface.get_rect(center=center)
            self.screen.blit(text_surface, text_rect)

    def draw_walls(self, board):
        # draw Horizontal Walls
        for r, c in board.horizontal_walls:
            rect = pygame.Rect(
                c * TILE_SIZE,
                (r + 1) * TILE_SIZE - (WALL_THICKNESS // 2),
                TILE_SIZE * 2,
                WALL_THICKNESS
            )
            pygame.draw.rect(self.screen, WALL_COLOR, rect)

        # draw Vertical Walls
        for r, c in board.vertical_walls:
            rect = pygame.Rect(
                (c + 1) * TILE_SIZE - (WALL_THICKNESS // 2),
                r * TILE_SIZE,
                WALL_THICKNESS,
                TILE_SIZE * 2
            )
            pygame.draw.rect(self.screen, WALL_COLOR, rect)

    def draw_side_panel(self,board ,p1_message, p2_message):
        panel_x = (BOARD_SIZE * TILE_SIZE) + 20
        if board.current_player.player_id == 1:
            p1_message = "Your Turn"
        elif board.current_player.player_id == 2:
            p2_message = "Your Turn"

        # --- Player 1 (Red) Top Area ---
        p1_color = (220, 20, 60)
        p1_title = self.title_font.render("Player 1", True, p1_color)
        self.screen.blit(p1_title, (panel_x, 50))

        if p1_message:
            p1_text = self.msg_font.render(p1_message, True, BLACK)
            self.screen.blit(p1_text, (panel_x, 80))

        # --- Player 2 (Blue) Bottom Area ---
        p2_color = (30, 144, 255)
        p2_title_y = (BOARD_SIZE * TILE_SIZE) - 100
        p2_title = self.title_font.render("Player 2", True, p2_color)
        self.screen.blit(p2_title, (panel_x, p2_title_y))

        if p2_message:
            p2_text = self.msg_font.render(p2_message, True, BLACK)
            self.screen.blit(p2_text, (panel_x, p2_title_y + 30))