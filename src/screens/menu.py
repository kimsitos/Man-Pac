import pygame
from src.screens.screen_base import ScreenBase, ScreenState


class Menu(ScreenBase):
    """Representa el menú principal."""

    def __init__(self):
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
        self.quit_text = self.font.render("QUIT", True, (255, 255, 255))
        self.quit_rect = self.quit_text.get_rect(center=(1200 // 2, 600))
        background = pygame.image.load(
            "assets/sprites/background_menu.jpg"
        ).convert()
        self.background = pygame.transform.scale(
            background,
            self.screen.get_size()
        )

    def event_cacher(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if self.state == ScreenState.MENU and event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_rect.collidepoint(event.pos):
                    self.request_state_change(ScreenState.PLAY)
                elif self.high_score_rect.collidepoint(event.pos):
                    self.request_state_change(ScreenState.HIGH_SCORE)
                elif self.quit_rect.collidepoint(event.pos):
                    return False
        return True

    def change_screen(self):
        target = self.consume_pending_state()
        if target is not None:
            return target
        return None

    def change_color_title(self):
        mouse_pos = pygame.mouse.get_pos()
        self.play_text = self._render_title(
            "PLAY", self.play_rect, (255, 255, 0), mouse_pos
        )
        self.high_score_text = self._render_title(
            "HIGH SCORE", self.high_score_rect, (255, 255, 0), mouse_pos
        )
        self.quit_text = self._render_title(
            "QUIT", self.quit_rect, (255, 0, 0), mouse_pos
        )

    def render(self):
        self.screen = pygame.display.get_surface()
        self.clear_screen()

        if self.state == ScreenState.MENU:
            self.screen.blit(self.background, (0, 0))

            self.change_color_title()
            self.screen.blit(self.play_text, self.play_rect)
            self.screen.blit(self.high_score_text, self.high_score_rect)
            self.screen.blit(self.quit_text, self.quit_rect)
