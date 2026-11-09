from abc import ABC, abstractmethod
from typing import Any
from enum import Enum
import pygame


class ScreenState(Enum):
    """
    This defines a set of possible game states as typed names: menu, playing,
      win, lose, mid-menu, and scores. Each has a string value used to
      identify the screen.
    """
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
        """
        This forces each screen to implement its own event handling, because
          each one reacts differently.
        """
        ...

    @abstractmethod
    def change_screen(self) -> str:
        """
        This forces each screen to implement how it decides whether to move to
          another screen, because each one has its own logic: menu, game, etc.
        """
        ...

    @abstractmethod
    def render(self) -> None:
        """
        All screens must have their own render, because the system
        treats them the same and each one draws different things
        """
        ...

    def request_state_change(self, next_state):
        """
        This function sends a request to the system to switch
          to another screen
        """
        print(f"Se ha solicitado un cambio de patalla a {next_state}")
        if next_state is not None and self.pending_state is None:
            self.pending_state = next_state

    def consume_pending_state(self):
        """
        This function checks if there is a pending screen transition,
          returns it, and deletes it so that it is not executed twice.
        """
        if self.pending_state is None:
            return None

        target = self.pending_state
        self.pending_state = None
        return target.value if isinstance(target, Enum) else target

    def clear_screen(self) -> None:
        """
        It takes the current screen again and paints it black to clear the
          previous frame before drawing the next screen.
        """
        self.screen = pygame.display.get_surface()
        self.screen.fill("black")

    def render_title(
        self,
        text: str,
        rect: Any,
        hover_color: tuple[int, int, int],
        mouse_pos: tuple[int, int],
    ) -> Any:
        """
        This function changes the text color of a button if the cursor is over
          the button's rectangle; otherwise, it leaves it white.
        """
        color = (
            hover_color
            if rect.collidepoint(mouse_pos)
            else (255, 255, 255)
        )
        return self.font.render(text, True, color)
