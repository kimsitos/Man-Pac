import pygame
from typing import TYPE_CHECKING, cast
from src.screens.screen_base import get_display_surface

if TYPE_CHECKING:
    from src.screens.game_screen import GameScreen


class Hubs:
    """

    Manage the in-game HUD shown below the maze.

    This class keeps the score, lives, and timer aligned in a single row and
    updates the layout whenever the window size changes or the values change.
    """

    def __init__(self, game_screen: "GameScreen") -> None:
        """
        Store the parent screen and initialize the HUD text and layout."""
        self.game_screen = game_screen
        self.screen = get_display_surface()
        self.font = pygame.font.Font(None, 50)
        self.spacing = 70
        self.horizontal_padding = 25
        self.score_text = self.font.render("score 0", True, (255, 255, 255))
        self.lives_text = self.font.render("lives 3", True, (255, 255, 255))
        self.time_text = self.font.render("Time ", True, (255, 255, 255))
        self.level_text = self.font.render("Level 1", True, (255, 255, 255))
        self._update_layout()

    def _get_total_width(self) -> int:
        """Return the total width of the HUD texts and their gaps."""
        texts = [self.score_text, self.lives_text, self.time_text,
                 self.level_text]
        return sum(cast(int, text.get_width())
                   for text in texts) + self.spacing * (
            len(texts) - 1
        )

    def _update_layout(self) -> None:
        """
        Recalculate the HUD positions so the three labels remain centered
        and readable on the current screen size.
        """
        screen = pygame.display.get_surface()
        if screen is None:
            return
        self.screen = screen

        total_width = self._get_total_width()
        start_x = max(
            (self.screen.get_width() - total_width) // 2,
            self.horizontal_padding
        )
        y = self.screen.get_height() - 40

        current_x = start_x
        self.score_rect = self.score_text.get_rect(midleft=(current_x, y))
        current_x += self.score_text.get_width() + self.spacing
        self.lives_rect = self.lives_text.get_rect(midleft=(current_x, y))
        current_x += self.lives_text.get_width() + self.spacing
        self.time_rect = self.time_text.get_rect(midleft=(current_x, y))
        current_x += self.time_text.get_width() + self.spacing
        self.level_rect = self.level_text.get_rect(midleft=(current_x, y))

    def get_required_width(self) -> int:
        """
        Return the minimum horizontal space needed by the HUD.

        This value is used to resize the game window so the maze and the HUD
        can coexist without clipping or overlapping.
        """
        self.level_text = self.font.render(
            f"Level {self.game_screen.level}", True, (255, 255, 255)
        )
        return self._get_total_width() + self.horizontal_padding * 2

    def render(self) -> None:
        """
        Refresh the HUD values from the game state and draw them on screen.
        """
        stats = self.game_screen.get_stats()
        self.score_text = self.font.render(
            f"score {stats['score']}", True, (255, 255, 255)
        )
        self.lives_text = self.font.render(
            f"lives {stats['lives']}", True, (255, 255, 255)
        )
        self.time_text = self.font.render(
            f"time  {stats['time']}", True, (255, 255, 255)
        )
        self.level_text = self.font.render(
            f"Level {stats['level']}", True, (255, 255, 255)
        )
        self._update_layout()

        self.screen.blit(self.score_text, self.score_rect)
        self.screen.blit(self.lives_text, self.lives_rect)
        self.screen.blit(self.time_text, self.time_rect)
        self.screen.blit(self.level_text, self.level_rect)
