from src.screens.screen_base import ScreenBase, ScreenState
from src.screens.high_score import new_record, Player
import pygame


class Lost_Game(ScreenBase):
    """pantalla de menu el juego"""

    def __init__(self):
        self.state = ScreenState.LOST_GAME
        self.writing_name = False
        self.player_name = ""
        self.score = 200
        self.input_font = pygame.font.Font(None, 100)
        self.font = pygame.font.Font(None, 150)
        self.menu_text = self.font.render("Menu", True, (255, 255, 255))
        self.menu_rect = self.menu_text.get_rect(center=(700, 1300))
        self.new_score_text = self.font.render(
            "New Score", True, (255, 255, 255))
        self.new_score_rect = self.new_score_text.get_rect(center=(700, 1200))
        self.screen = pygame.display.get_surface()
        background = pygame.image.load(
            "assets/sprites/background_lost_game.png"
        ).convert()
        self.background = pygame.transform.scale(
            background,
            self.screen.get_size()
        )

    def event_cacher(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.menu_rect.collidepoint(event.pos):
                    self.state = ScreenState.MENU
                if self.new_score_rect.collidepoint(event.pos):
                    self.writing_name = True
            if self.writing_name:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        new_record(
                            Player(name=self.player_name, scored=self.score)
                        )
                        self.state = ScreenState.MENU
                    elif event.key == pygame.K_BACKSPACE:
                        self.player_name = self.player_name[:-1]
                    elif len(self.player_name) < 10:
                        self.player_name += event.unicode
        return True

    def change_screen(self):
        if self.state == ScreenState.LOST_GAME:
            return None

        next_state = self.state.value
        self.state = ScreenState.LOST_GAME
        return next_state

    def change_color_title(self):
        mouse_pos = pygame.mouse.get_pos()

        self.menu_text = self._render_title(
            "Menu", self.menu_rect, (255, 255, 0), mouse_pos
        )
        self.new_score_text = self._render_title(
            "New Score", self.new_score_rect, (255, 255, 0), mouse_pos
        )

    def render(self):
        self.clear_screen()

        if self.state == ScreenState.LOST_GAME:
            self.screen.blit(self.background, (0, 0))

            self.change_color_title()

            self.screen.blit(self.menu_text, self.menu_rect)
            self.screen.blit(self.new_score_text, self.new_score_rect)

        if self.writing_name:
            pygame.draw.rect(
                self.screen,
                (255, 255, 255),
                (350, 1000, 700, 100),
                3
            )

            input_surface = self.input_font.render(
                self.player_name,
                True,
                (255, 255, 255)
            )

            self.screen.blit(input_surface, (360, 1020))
