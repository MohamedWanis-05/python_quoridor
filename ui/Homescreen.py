import pygame
from game.constants import WINDOW_WIDTH, WINDOW_HEIGHT, WHITE, BLACK, BOARD_COLOR


class HomeScreen:
    def __init__(self, screen):
        self.screen = screen
        pygame.font.init()
        self.title_font = pygame.font.SysFont(None, 80)
        self.small_font = pygame.font.SysFont(None, 35)
        self.button_font = pygame.font.SysFont(None, 50)

        self.selected_mode = "1v1"
        self.selected_size = 9

        # --- NEW: Added difficulty variable ---
        self.selected_difficulty = "Easy"

        center_x = WINDOW_WIDTH // 2

        self.btn_1v1 = pygame.Rect(center_x - 150, 230, 140, 60)
        self.btn_1vai = pygame.Rect(center_x + 10, 230, 140, 60)

        # --- NEW: Added difficulty button rect ---
        self.btn_difficulty = pygame.Rect(center_x - 100, 310, 200, 40)

        button_width = 100
        gap = 20
        start_x = center_x - (button_width * 1.5 + gap)

        # --- UPDATED: Pushed these down from 340 to 380 ---
        self.btn_5x5 = pygame.Rect(start_x, 380, button_width, 60)
        self.btn_7x7 = pygame.Rect(start_x + button_width + gap, 380, button_width, 60)
        self.btn_9x9 = pygame.Rect(start_x + 2 * (button_width + gap), 380, button_width, 60)

        # --- UPDATED: Pushed this down from 480 to 500 ---
        self.btn_start = pygame.Rect(center_x - 100, 500, 200, 70)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = event.pos

                if self.btn_1v1.collidepoint(mouse_pos):
                    self.selected_mode = "1v1"
                elif self.btn_1vai.collidepoint(mouse_pos):
                    self.selected_mode = "1vAI"

                # --- NEW: Difficulty click logic (Cycles Easy -> Medium -> Hard) ---
                elif self.selected_mode == "1vAI" and self.btn_difficulty.collidepoint(mouse_pos):
                    if self.selected_difficulty == "Easy":
                        self.selected_difficulty = "Medium"
                    elif self.selected_difficulty == "Medium":
                        self.selected_difficulty = "Hard"
                    else:
                        self.selected_difficulty = "Easy"

                elif self.btn_5x5.collidepoint(mouse_pos):
                    self.selected_size = 5
                elif self.btn_7x7.collidepoint(mouse_pos):
                    self.selected_size = 7
                elif self.btn_9x9.collidepoint(mouse_pos):
                    self.selected_size = 9

                elif self.btn_start.collidepoint(mouse_pos):
                    return {
                        "mode": self.selected_mode,
                        "size": self.selected_size,
                        "difficulty": self.selected_difficulty
                    }

        return None

    def draw(self):
        self.screen.fill(WHITE)

        title_text = self.title_font.render("QUORIDOR", True, BLACK)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 120))
        self.screen.blit(title_text, title_rect)

        color_1v1 = BOARD_COLOR if self.selected_mode == "1v1" else (200, 200, 200)
        color_1vai = BOARD_COLOR if self.selected_mode == "1vAI" else (200, 200, 200)

        pygame.draw.rect(self.screen, color_1v1, self.btn_1v1, border_radius=10)
        pygame.draw.rect(self.screen, color_1vai, self.btn_1vai, border_radius=10)

        text_1v1 = self.button_font.render("1 v 1", True, BLACK)
        text_1vai = self.button_font.render("1 v AI", True, BLACK)

        self.screen.blit(text_1v1, text_1v1.get_rect(center=self.btn_1v1.center))
        self.screen.blit(text_1vai, text_1vai.get_rect(center=self.btn_1vai.center))

        # --- NEW: Draw Difficulty Button (ONLY IF 1vAI IS SELECTED) ---
        if self.selected_mode == "1vAI":
            if self.selected_difficulty == "Easy":
                diff_color = (100, 200, 100)  # Green
            elif self.selected_difficulty == "Medium":
                diff_color = (255, 165, 0)  # Orange
            elif self.selected_difficulty == "Hard":
                diff_color = (255, 100, 100)  # Red

            pygame.draw.rect(self.screen, diff_color, self.btn_difficulty, border_radius=8)
            diff_text = self.small_font.render(f"Difficulty: {self.selected_difficulty}", True, WHITE)
            self.screen.blit(diff_text, diff_text.get_rect(center=self.btn_difficulty.center))

        # --- Draw Size Buttons ---
        color_5x5 = BOARD_COLOR if self.selected_size == 5 else (200, 200, 200)
        color_7x7 = BOARD_COLOR if self.selected_size == 7 else (200, 200, 200)
        color_9x9 = BOARD_COLOR if self.selected_size == 9 else (200, 200, 200)

        pygame.draw.rect(self.screen, color_5x5, self.btn_5x5, border_radius=10)
        pygame.draw.rect(self.screen, color_7x7, self.btn_7x7, border_radius=10)
        pygame.draw.rect(self.screen, color_9x9, self.btn_9x9, border_radius=10)

        text_5x5 = self.button_font.render("5x5", True, BLACK)
        text_7x7 = self.button_font.render("7x7", True, BLACK)
        text_9x9 = self.button_font.render("9x9", True, BLACK)

        self.screen.blit(text_5x5, text_5x5.get_rect(center=self.btn_5x5.center))
        self.screen.blit(text_7x7, text_7x7.get_rect(center=self.btn_7x7.center))
        self.screen.blit(text_9x9, text_9x9.get_rect(center=self.btn_9x9.center))

        # --- Draw Start Button ---
        pygame.draw.rect(self.screen, (46, 204, 113), self.btn_start, border_radius=10)  # Green Start Button
        text_start = self.button_font.render("START", True, WHITE)
        self.screen.blit(text_start, text_start.get_rect(center=self.btn_start.center))