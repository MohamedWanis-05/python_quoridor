import pygame
from game.constants import WINDOW_WIDTH, WINDOW_HEIGHT, WHITE, BLACK, BOARD_COLOR


class HomeScreen:
    def __init__(self, screen):
        self.screen = screen
        pygame.font.init()
        self.title_font = pygame.font.SysFont(None, 80)
        self.button_font = pygame.font.SysFont(None, 50)

        self.selected_mode = "1v1"

        center_x = WINDOW_WIDTH // 2

        self.btn_1v1 = pygame.Rect(center_x - 150, 300, 140, 60)
        self.btn_1vai = pygame.Rect(center_x + 10, 300, 140, 60)

        self.btn_start = pygame.Rect(center_x - 100, 450, 200, 70)

    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = event.pos

                if self.btn_1v1.collidepoint(mouse_pos):
                    self.selected_mode = "1v1"
                elif self.btn_1vai.collidepoint(mouse_pos):
                    self.selected_mode = "1vAI"

                elif self.btn_start.collidepoint(mouse_pos):
                    return self.selected_mode

        return None

    def draw(self):
        self.screen.fill(WHITE)

        title_text = self.title_font.render("QUORIDOR", True, BLACK)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 150))
        self.screen.blit(title_text, title_rect)

        color_1v1 = BOARD_COLOR if self.selected_mode == "1v1" else (200, 200, 200)
        color_1vai = BOARD_COLOR if self.selected_mode == "1vAI" else (200, 200, 200)

        pygame.draw.rect(self.screen, color_1v1, self.btn_1v1, border_radius=10)
        pygame.draw.rect(self.screen, color_1vai, self.btn_1vai, border_radius=10)

        text_1v1 = self.button_font.render("1 v 1", True, BLACK)
        text_1vai = self.button_font.render("1 v AI", True, BLACK)

        self.screen.blit(text_1v1, text_1v1.get_rect(center=self.btn_1v1.center))
        self.screen.blit(text_1vai, text_1vai.get_rect(center=self.btn_1vai.center))

        # Draw Start Button
        pygame.draw.rect(self.screen, (46, 204, 113), self.btn_start, border_radius=10)  # Green Start Button
        text_start = self.button_font.render("START", True, WHITE)
        self.screen.blit(text_start, text_start.get_rect(center=self.btn_start.center))