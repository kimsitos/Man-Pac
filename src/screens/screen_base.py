from abc import ABC, abstractmethod
from typing import Any
from enum import Enum
import pygame


class ScreenState(Enum):
    MENU = "MENU"
    PLAY = "PLAY"
    WIN_GAME = "WIN_GAME"
    LOST_GAME = "LOST_GAME"
    MENU_GAME = "MENU_GAME"
    HIGH_SCORE = "HIGH_SCORE"


class ScreenBase(ABC):
    def __init__(self):
        self.pending_state = None

    @abstractmethod
    def event_cacher(self) -> None:
        ...

    @abstractmethod
    def change_screen(self) -> str:
        ...

    @abstractmethod
    def render(self) -> None:
        ...

    def request_state_change(self, next_state):
        if next_state is not None:
            self.pending_state = next_state

    def consume_pending_state(self):
        if self.pending_state is None:
            return None

        target = self.pending_state
        self.pending_state = None
        return target.value if isinstance(target, Enum) else target

    def clear_screen(self) -> None:
        self.screen = pygame.display.get_surface()
        self.screen.fill("black")

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
