import pygame
from game.constants import TILE_SIZE, WHITE, BLACK, WALL_THICKNESS, WALL_COLOR


class Renderer:
    def __init__(self, screen):
        self.screen = screen
        pygame.font.init()
        self.font = pygame.font.SysFont(None, int(TILE_SIZE * 0.5))

        self.msg_font = pygame.font.SysFont(None, 28)
        self.title_font = pygame.font.SysFont(None, 32)
        self.btn_font = pygame.font.SysFont(None, 24)

        self.btn_menu = pygame.Rect(0, 0, 0, 0)
        self.btn_reset = pygame.Rect(0, 0, 0, 0)

    def draw(self, board, p1_message="", p2_message="", p1_message_color=(0, 0, 0), p2_message_color=(0, 0, 0),
             hovered_wall=None, valid_moves=None):
        if valid_moves is None:
            valid_moves = []

        self.screen.fill(WHITE)
        self.draw_grid(board)
        self.draw_valid_moves(valid_moves)

        self.draw_players(board)
        self.draw_walls(board)
        self.draw_side_panel(board, p1_message, p2_message, p1_message_color, p2_message_color)
        self.draw_buttons(board)

        if hovered_wall:
            self.draw_ghost_wall(hovered_wall)

    def draw_ghost_wall(self, hovered_wall):
        r, c, is_horizontal = hovered_wall

        if is_horizontal:
            rect_w = TILE_SIZE * 2
            rect_h = WALL_THICKNESS
            rect_x = c * TILE_SIZE
            rect_y = (r + 1) * TILE_SIZE - (WALL_THICKNESS // 2)
        else:
            rect_w = WALL_THICKNESS
            rect_h = TILE_SIZE * 2
            rect_x = (c + 1) * TILE_SIZE - (WALL_THICKNESS // 2)
            rect_y = r * TILE_SIZE
        ghost_surface = pygame.Surface((rect_w, rect_h), pygame.SRCALPHA)
        ghost_surface.fill((*WALL_COLOR, 128))
        self.screen.blit(ghost_surface, (rect_x, rect_y))

    def draw_grid(self, board):
        for row in range(board.size):
            for col in range(board.size):
                rect = pygame.Rect(
                    col * TILE_SIZE,
                    row * TILE_SIZE,
                    TILE_SIZE,
                    TILE_SIZE
                )
                pygame.draw.rect(self.screen, BLACK, rect, 1)

    def draw_valid_moves(self, valid_moves):
        for move in valid_moves:
            if isinstance(move, tuple):
                row, col = move
                center = (
                    col * TILE_SIZE + TILE_SIZE // 2,
                    row * TILE_SIZE + TILE_SIZE // 2
                )
                pygame.draw.circle(self.screen, (0, 255, 0), center, 10)

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
        for r, c in board.horizontal_walls:
            rect = pygame.Rect(
                c * TILE_SIZE,
                (r + 1) * TILE_SIZE - (WALL_THICKNESS // 2),
                TILE_SIZE * 2,
                WALL_THICKNESS
            )
            pygame.draw.rect(self.screen, WALL_COLOR, rect)

        for r, c in board.vertical_walls:
            rect = pygame.Rect(
                (c + 1) * TILE_SIZE - (WALL_THICKNESS // 2),
                r * TILE_SIZE,
                WALL_THICKNESS,
                TILE_SIZE * 2
            )
            pygame.draw.rect(self.screen, WALL_COLOR, rect)

    def draw_side_panel(self, board, p1_message, p2_message, p1_message_color=(0, 0, 0), p2_message_color=(0, 0, 0)):
        panel_x = (board.size * TILE_SIZE) + 20

        # --- Player 1 (Red) Top Area ---
        p1_color = (220, 20, 60)
        p1_title = self.title_font.render("Player 1", True, p1_color)
        self.screen.blit(p1_title, (panel_x, 50))

        if p1_message:
            p1_text = self.msg_font.render(p1_message, True, p1_message_color)
            self.screen.blit(p1_text, (panel_x, 80))

        # --- Player 2 (Blue) Bottom Area ---
        p2_color = (30, 144, 255)
        p2_title_y = (board.size * TILE_SIZE) - 100
        p2_title = self.title_font.render("Player 2", True, p2_color)
        self.screen.blit(p2_title, (panel_x, p2_title_y))

        if p2_message:
            p2_text = self.msg_font.render(p2_message, True, p2_message_color)
            self.screen.blit(p2_text, (panel_x, p2_title_y + 30))

    def draw_buttons(self, board):

        button_y = (board.size * TILE_SIZE) + 40

        self.btn_menu = pygame.Rect(20, button_y, 140, 40)
        self.btn_reset = pygame.Rect(180, button_y, 140, 40)
        # Menu Button
        pygame.draw.rect(self.screen, (220, 220, 220), self.btn_menu, border_radius=5)
        pygame.draw.rect(self.screen, BLACK, self.btn_menu, 2, border_radius=5)
        menu_text = self.btn_font.render("Main Menu", True, BLACK)
        self.screen.blit(menu_text, menu_text.get_rect(center=self.btn_menu.center))

        # Reset Button
        pygame.draw.rect(self.screen, (220, 220, 220), self.btn_reset, border_radius=5)
        pygame.draw.rect(self.screen, BLACK, self.btn_reset, 2, border_radius=5)
        reset_text = self.btn_font.render("Reset Game", True, BLACK)
        self.screen.blit(reset_text, reset_text.get_rect(center=self.btn_reset.center))