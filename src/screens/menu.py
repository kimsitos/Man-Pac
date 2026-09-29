import pygame
from enum import Enum
from typing import Any, ClassVar

from pydantic import BaseModel


class StateMachine(Enum):
    MENU = "MENU"
    PLAY = "PLAY"
    QUIT = "QUIT"
    HIGH_SCORE = "HIGH_SCORE"


class Menu(BaseModel):
    """Representa el menú principal."""

    play_rect: Any = None
    play_text: Any = None
    high_score_rect: Any = None
    high_score_text: Any = None
    quit_text: Any = None
    quit_rect: Any = None
    state: StateMachine = StateMachine.MENU
    width: ClassVar[int] = 1200
    height: ClassVar[int] = 1000
    font: Any = None

    def init_menu(self):

        self.font = pygame.font.Font(None, 100)
        self.play_text = self.font.render("JUGAR", True, (255, 255, 255))
        self.play_rect = self.play_text.get_rect(center=(self.width // 2, 300))
        self.high_score_text = self.font.render(
            "HIGH SCORE", True, (255, 255, 255))
        self.high_score_rect = self.high_score_text.get_rect(
            center=(self.width // 2, 500))
        self.quit_text = self.font.render("QUIT", True, (255, 255, 255))
        self.quit_rect = self.quit_text.get_rect(center=(self.width // 2, 700))

    def change_color_title(self):
        # Cambiar color si el ratón está encima
        if self.play_rect.collidepoint(pygame.mouse.get_pos()):
            self.play_text = self.font.render("JUGAR", True, (255, 255, 0))
        else:
            self.play_text = self.font.render("JUGAR", True, (255, 255, 255))

        if self.high_score_rect.collidepoint(pygame.mouse.get_pos()):
            self.high_score_text = self.font.render(
                "HIGH SCORE", True, (255, 255, 0))
        else:
            self.high_score_text = self.font.render(
                "HIGH SCORE", True, (255, 255, 255))

        if self.quit_rect.collidepoint(pygame.mouse.get_pos()):
            self.quit_text = self.font.render("QUIT", True, (255, 0, 0))
        else:
            self.quit_text = self.font.render("QUIT", True, (255, 255, 255))

    def menu_render(self):

        screen = pygame.display.set_mode((self.width, self.height))
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if self.state == StateMachine.MENU:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.play_rect.collidepoint(event.pos):
                            self.state = StateMachine.PLAY
                        if self.high_score_rect.collidepoint(event.pos):
                            self.state = StateMachine.HIGH_SCORE
                        if self.quit_rect.collidepoint(event.pos):
                            self.state = StateMachine.QUIT

            screen.fill((0, 0, 0))

            if self.state == StateMachine.MENU:
                self.change_color_title()
                screen.blit(self.play_text, self.play_rect)
                screen.blit(self.high_score_text, self.high_score_rect)
                screen.blit(self.quit_text, self.quit_rect)
            elif self.state == StateMachine.PLAY:
                texto = self.font.render("PACMAN INICIADO", True, (0, 255, 0))
                screen.blit(texto, (180, 250))
            elif self.state == StateMachine.HIGH_SCORE:
                texto = self.font.render(
                    "HIGH SCORE INICIADO", True, (0, 255, 0))
                screen.blit(texto, (180, 250))
            elif self.state == StateMachine.QUIT:
                running = False
                return

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()


def menu_run():
    pygame.init()
    menu = Menu()
    menu.init_menu()
    menu.menu_render()


if __name__ == "__main__":
    menu_run()
