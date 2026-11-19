from src.screens.screen_base import (
    ScreenBase,
    ScreenState,
    get_display_surface,
)
from src.screens.high_score import is_high_score, new_record, Player
from typing import Any
import pygame


class Lost_Game(ScreenBase):
    """Defeat screen with save-score and return-to-menu options."""

    def __init__(self) -> None:
        """Initialize the defeat screen and its buttons."""
        super().__init__()
        self.state = ScreenState.LOST_GAME
        self.writing_name = False
        self.player_name = ""
        self.score = 0
        self._checked_score: int | None = None
        self.can_add_score = False
        self.lit = pygame.font.Font(None, 50)
        self.input_font = pygame.font.Font(None, 100)
        self.font = pygame.font.Font(None, 120)
        self.score_text = self.lit.render(
            f"Score: {self.score}", True, (0, 0, 0))
        self.score_rect = self.score_text.get_rect(center=(600, 250))
        self.check_text = self.lit.render(
            "Check top 10", True, (255, 255, 255))
        self.check_rect = self.check_text.get_rect(center=(1050, 950))
        self.menu_text = self.font.render("Menu", True, (255, 255, 255))
        self.menu_rect = self.menu_text.get_rect(center=(600, 900))
        self.new_score_text = self.font.render(
            "New Score", True, (255, 255, 255))
        self.new_score_rect = self.new_score_text.get_rect(center=(600, 800))
        self.screen = get_display_surface()
        background = pygame.image.load(
            "assets/sprites/background_lost_game.jpg"
        ).convert()
        self.background = pygame.transform.scale(
            background,
            self.screen.get_size()
        )

    def event_cacher(self) -> Any:
        """Handle clicks and keyboard input to return or save the score."""
        self._update_score_eligibility()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if (
                self.state == ScreenState.LOST_GAME
                and event.type == pygame.MOUSEBUTTONDOWN
            ):
                if self.menu_rect.collidepoint(event.pos):
                    self.request_state_change(ScreenState.MENU)
                elif self.check_rect.collidepoint(event.pos):
                    self.request_state_change(ScreenState.HIGH_SCORE)
                elif (
                    self.can_add_score
                    and self.new_score_rect.collidepoint(event.pos)
                ):
                    self.writing_name = True
            if self.writing_name:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        new_record(
                            Player(name=self.player_name, scored=self.score)
                        )
                        self.player_name = ""
                        self.score = 0
                        self.writing_name = False
                    elif event.key == pygame.K_BACKSPACE:
                        self.player_name = self.player_name[:-1]
                    elif len(self.player_name) < 10:
                        self.player_name += event.unicode
        return True

    def _update_score_eligibility(self) -> None:
        if self._checked_score != self.score:
            self.can_add_score = is_high_score(self.score)
            self._checked_score = self.score

    def change_screen(self) -> Any:
        """Process the pending state change for the defeat screen."""
        target = self.consume_pending_state()
        if target is not None:
            return target
        return None

    def change_color_title(self) -> None:
        """Highlight the option under the mouse cursor."""
        mouse_pos = pygame.mouse.get_pos()

        self.menu_text = self.render_title(
            "Menu", self.menu_rect, (255, 255, 0), mouse_pos
        )
        self.new_score_text = self.render_title(
            "New Score", self.new_score_rect, (255, 255, 0), mouse_pos
        )
        check_color = (
            (135, 206, 235)
            if self.check_rect.collidepoint(mouse_pos)
            else (255, 255, 255)
        )
        self.check_text = self.lit.render(
            "Check top 10", True, check_color
        )
        self.score_text = self.lit.render(
            f"Score: {self.score}", True, (0, 0, 0))

    def render(self) -> None:
        """Draw the defeat screen and the name input field when needed."""
        self._update_score_eligibility()
        self.screen = get_display_surface()
        self.clear_screen()

        if self.state == ScreenState.LOST_GAME:
            self.screen.blit(self.background, (0, 0))

            self.change_color_title()
            self.screen.blit(self.score_text, self.score_rect)
            self.screen.blit(self.menu_text, self.menu_rect)
            self.screen.blit(self.check_text, self.check_rect)

        if self.can_add_score:
            self.screen.blit(self.new_score_text, self.new_score_rect)

        if self.writing_name:
            pygame.draw.rect(
                self.screen,
                (255, 255, 255),
                (260, 650, 700, 100),
                3
            )

            input_surface = self.input_font.render(
                self.player_name,
                True,
                (255, 255, 255)
            )

            self.screen.blit(input_surface, (270, 670))
