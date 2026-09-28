import pygame
from enum import Enum
from typing import Any

from pydantic import BaseModel


class StateMachine(Enum):
    MENU = "MENU"
    PLAY = "PLAY"
    HIGH_SCORE = "HIGH_SCORE"


class Menu(BaseModel):
    """Representa el menú principal."""

    play_rect: Any = None
    high_score_rect: Any = None
    quit_rect: Any = None
    state: StateMachine = StateMachine.MENU

    def render_menu(self):
        pygame.init()

        width, height = 1200, 1000
        screen = pygame.display.set_mode((width, height))
        font = pygame.font.Font(None, 100)

        play_text = font.render("JUGAR", True, (255, 255, 255))
        self.play_rect = play_text.get_rect(center=(width // 2, 700))

        high_score_text = font.render("HIGH SCORE", True, (255, 255, 255))
        self.high_score_rect = high_score_text.get_rect(center=(width // 2, 500))

        quit_text = font.render("QUIT", True, (255, 255, 255))
        self.quit_rect = quit_text.get_rect(center=(width // 2, 300))

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill((0, 0, 0))
            screen.blit(play_text, self.play_rect)
            screen.blit(high_score_text, self.high_score_rect)
            screen.blit(quit_text, self.quit_rect)
            pygame.display.flip()

        pygame.quit()


def menu_ms():
    return Menu().render_menu()

