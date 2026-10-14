from abc import ABC, abstractmethod
from typing import Any
from enum import Enum


class ScreenState(Enum):
    MENU = "MENU"
    PLAY = "PLAY"
    MENU_GAME = "MENU_GAME"
    HIGH_SCORE = "HIGH_SCORE"


class ScreenBase(ABC):
    @abstractmethod
    def event_cacher(self) -> None:
        ...

    @abstractmethod
    def change_screen(self) -> str:
        ...

    @abstractmethod
    def render(self) -> None:
        ...

    def clear_screen(self) -> None:
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
