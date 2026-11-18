import pygame
from typing import Any
from src.screens.screen_base import ScreenBase, ScreenState


class Menu(ScreenBase):
    """Main menu screen with start, score, and quit buttons."""

    def __init__(self) -> None:
        """Initialize the menu background and button positions."""
        super().__init__()
        self.state = ScreenState.MENU
        self.screen = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 100)
        self.play_text = self.font.render("PLAY", True, (255, 255, 255))
        self.play_rect = self.play_text.get_rect(center=(1200 // 2, 400))
        self.high_score_text = self.font.render(
            "HIGH SCORE", True, (255, 255, 255))
        self.high_score_rect = self.high_score_text.get_rect(
            center=(1200 // 2, 500))
        self.ins_text = self.font.render("INSTRUCTIONS", True, (255, 255, 255))
        self.ins_rect = self.ins_text.get_rect(center=(1200 // 2, 600))
        self.quit_text = self.font.render("QUIT", True, (255, 255, 255))
        self.quit_rect = self.quit_text.get_rect(center=(1200 // 2, 700))
        background = pygame.image.load(
            "assets/sprites/background_menu.jpg"
        ).convert()
        self.background = pygame.transform.scale(
            background,
            self.screen.get_size()
        )

    def event_cacher(self) -> Any:
        """Handle mouse clicks and prepare the screen transition."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if self.state == ScreenState.MENU:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.play_rect.collidepoint(event.pos):
                        self.request_state_change(ScreenState.PLAY)
                    elif self.high_score_rect.collidepoint(event.pos):
                        self.request_state_change(ScreenState.HIGH_SCORE)
                    elif self.ins_rect.collidepoint(event.pos):
                        self.request_state_change(ScreenState.INSTRUCTIONS)
                    elif self.quit_rect.collidepoint(event.pos):
                        return False
        return True

    def change_screen(self) -> Any:
        """Return the requested screen after the player clicks."""
        target = self.consume_pending_state()
        if target is not None:
            return target
        return None

    def change_color_title(self) -> None:
        """Change the hovered button color when the mouse is over it."""
        mouse_pos = pygame.mouse.get_pos()
        self.play_text = self.render_title(
            "PLAY", self.play_rect, (255, 255, 0), mouse_pos
        )
        self.high_score_text = self.render_title(
            "HIGH SCORE", self.high_score_rect, (255, 255, 0), mouse_pos
        )
        self.quit_text = self.render_title(
            "QUIT", self.quit_rect, (255, 0, 0), mouse_pos
        )
        self.ins_text = self.render_title(
            "INSTRUCTIONS", self.ins_rect, (50, 155, 150), mouse_pos
        )

    def render(self) -> None:
        """Draw the background and menu text each frame."""
        self.screen = pygame.display.get_surface()
        self.clear_screen()

        if self.state == ScreenState.MENU:
            self.screen.blit(self.background, (0, 0))

            self.change_color_title()
            self.screen.blit(self.ins_text, self.ins_rect)
            self.screen.blit(self.play_text, self.play_rect)
            self.screen.blit(self.high_score_text, self.high_score_rect)
            self.screen.blit(self.quit_text, self.quit_rect)
