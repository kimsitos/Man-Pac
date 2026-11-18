import pygame
from typing import Any
from src.screens.screen_base import (
    ScreenBase,
    ScreenState,
    get_display_surface,
)

TEXT = """                                         PAC-MAN - HOW TO PLAY
________________________________________________________________

Your goal is to collect all the dots in the maze without getting
caught by the ghosts!

Controls: Use W, A, S, D or the arrow keys to move around the maze.
[scape] - Pause the game

Cheat Mode...
M - Skip level
G - Activate/Deactivate Freeze ghosts
I - Activate/Deactivate invencibility

Collect dots: Eat all the small dots to earn points.
Avoid ghosts: Be careful! If a ghost catches you, you lose a life.
Power pellets: Eat the big dots to gain the ability to eat ghosts for a
few seconds.

Try to get the highest score and complete the maze. Good luck!"""


class InstructionsScreen(ScreenBase):
    """Screen that displays the game instructions to the player."""
    def __init__(self) -> None:
        super().__init__()
        self.state = ScreenState.INSTRUCTIONS
        self.screen = get_display_surface()
        self.font = pygame.font.Font(None, 100)
        self.small_font = pygame.font.Font(None, 40)
        self.ins_text = self.small_font.render(
            f"{TEXT}", True, (255, 255, 255))
        self.ins_rect = self.ins_text.get_rect(center=(1200 // 2, 500))
        self.menu_text = self.font.render("Menu", True, (255, 255, 255))
        self.menu_rect = self.menu_text.get_rect(center=(600, 950))

    def event_cacher(self) -> bool:
        """Handle clicks to continue the game or return to the menu."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.state == ScreenState.INSTRUCTIONS:
                    if self.menu_rect.collidepoint(event.pos):
                        self.request_state_change(ScreenState.MENU)

        return True

    def change_screen(self) -> str | None:
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

    def render(self) -> None:
        self.screen = get_display_surface()
        self.clear_screen()

        if self.state == ScreenState.INSTRUCTIONS:
            self.change_color_title()
            self.screen.blit(self.menu_text, self.menu_rect)
            self.screen.blit(self.ins_text, self.ins_rect)
