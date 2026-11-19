from src.screens.screen_base import (
    ScreenBase,
    ScreenState,
    get_display_surface,
)
from typing import Any
import pygame


class Menu_Game(ScreenBase):
    """Pause screen with continue and return-to-menu actions."""

    def __init__(self) -> None:
        """Create the pause menu and its two main buttons."""
        super().__init__()
        self.state = ScreenState.MENU_GAME
        self.font = pygame.font.Font(None, 120)
        self.menu_text = self.font.render("Menu", True, (255, 255, 255))
        self.menu_rect = self.menu_text.get_rect(center=(600, 690))
        self.continue_text = self.font.render(
            "Continue", True, (255, 255, 255))
        self.continue_rect = self.continue_text.get_rect(center=(600, 600))
        self.screen = get_display_surface()
        background = pygame.image.load(
            "assets/sprites/background_high_score.jpg"
        ).convert()
        self.background = pygame.transform.scale(
            background,
            self.screen.get_size()
        )

    def event_cacher(self) -> Any:
        """Handle keyboard and mouse input for the pause menu."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if (
                event.type == pygame.KEYUP
                and event.key == pygame.K_ESCAPE
            ):
                self.request_state_change(ScreenState.PLAY)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.state == ScreenState.MENU_GAME:
                    if self.menu_rect.collidepoint(event.pos):
                        self.request_state_change(ScreenState.MENU)
                    elif self.continue_rect.collidepoint(event.pos):
                        self.request_state_change(ScreenState.PLAY)

        return True

    def change_screen(self) -> Any:
        """Consume the pending transition after the player choice."""
        target = self.consume_pending_state()
        if target is not None:
            return target
        return None

    def change_color_title(self) -> None:
        """Highlight the hovered option for visual feedback."""
        mouse_pos = pygame.mouse.get_pos()

        self.menu_text = self.render_title(
            "Menu", self.menu_rect, (255, 255, 0), mouse_pos
        )
        self.continue_text = self.render_title(
            "Continue", self.continue_rect, (255, 255, 0), mouse_pos
        )

    def render(self) -> None:
        """Draw the pause screen with its background and buttons."""
        self.screen = get_display_surface()
        self.clear_screen()

        if self.state == ScreenState.MENU_GAME:
            self.screen.blit(self.background, (0, 0))
            self.change_color_title()
            self.screen.blit(self.menu_text, self.menu_rect)
            self.screen.blit(self.continue_text, self.continue_rect)
