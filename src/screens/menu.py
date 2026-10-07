from enum import Enum
from typing import Any, ClassVar

import pygame

from src.screens.screen_base import ScreenBase


class StateMachine(Enum):
    MENU = "MENU"
    PLAY = "PLAY"
    HIGH_SCORE = "HIGH_SCORE"


class Menu(ScreenBase):
    """Representa el menú principal."""

    width: ClassVar[int] = 1200
    height: ClassVar[int] = 1000

    def __init__(self):
        self.state = StateMachine.MENU
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.Font(None, 100)
        self.play_text = self.font.render("JUGAR", True, (255, 255, 255))
        self.play_rect = self.play_text.get_rect(center=(self.width // 2, 300))
        self.high_score_text = self.font.render(
            "HIGH SCORE", True, (255, 255, 255))
        self.high_score_rect = self.high_score_text.get_rect(
            center=(self.width // 2, 500))
        self.quit_text = self.font.render("QUIT", True, (255, 255, 255))
        self.quit_rect = self.quit_text.get_rect(center=(self.width // 2, 700))

    def event_cacher(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if self.state == StateMachine.MENU:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.play_rect.collidepoint(event.pos):
                        self.state = StateMachine.PLAY
                    elif self.high_score_rect.collidepoint(event.pos):
                        self.state = StateMachine.HIGH_SCORE
                    elif self.quit_rect.collidepoint(event.pos):
                        return False
        return True

    def change_screen(self):
        if self.state == StateMachine.MENU:
            return None

        next_state = self.state.value
        self.state = StateMachine.MENU
        return next_state

    def clear_screen(self) -> None:
        self.screen.fill((0, 0, 0))

    def change_color_title(self):
        mouse_pos = pygame.mouse.get_pos()
        self.play_text = self._render_title(
            "JUGAR", self.play_rect, (255, 255, 0), mouse_pos
        )
        self.high_score_text = self._render_title(
            "HIGH SCORE", self.high_score_rect, (255, 255, 0), mouse_pos
        )
        self.quit_text = self._render_title(
            "QUIT", self.quit_rect, (255, 0, 0), mouse_pos
        )

    def _render_title(
        self,
        text: str,
        rect: Any,
        hover_color: tuple[int, int, int],
        mouse_pos: tuple[int, int],
    ) -> Any:
        color = (
            hover_color
            if rect.collidepoint(mouse_pos)
            else (255, 255, 255)
        )
        return self.font.render(text, True, color)

    def render(self):
        self.clear_screen()

        if self.state == StateMachine.MENU:
            self.change_color_title()
            self.screen.blit(self.play_text, self.play_rect)
            self.screen.blit(self.high_score_text, self.high_score_rect)
            self.screen.blit(self.quit_text, self.quit_rect)
