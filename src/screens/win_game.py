from src.screens.screen_base import ScreenBase, ScreenState
from src.screens.high_score import is_high_score, new_record, Player
import pygame


class Win_Game(ScreenBase):
    """Victory screen with score submission and return-to-menu actions."""

    def __init__(self):
        """Initialize the victory screen and its buttons."""
        super().__init__()
        self.state = ScreenState.WIN_GAME
        self.writing_name = False
        self.player_name = ""
        self.score = 0
        self._checked_score: int | None = None
        self.can_add_score = False
        self.lit = pygame.font.Font(None, 50)
        self.input_font = pygame.font.Font(None, 100)
        self.font = pygame.font.Font(None, 120)
        self.Check_text = self.lit.render(
            "Check top 10", True, (255, 255, 255))
        self.Check_rect = self.Check_text.get_rect(center=(1050, 950))
        self.win_text = self.font.render("You Win!", True, (255, 255, 255))
        self.win_rect = self.win_text.get_rect(center=(600, 200))
        self.menu_text = self.font.render("Menu", True, (255, 255, 255))
        self.menu_rect = self.menu_text.get_rect(center=(600, 900))
        self.new_score_text = self.font.render(
            "New Score", True, (255, 255, 255))
        self.new_score_rect = self.new_score_text.get_rect(center=(600, 800))
        self.screen = pygame.display.get_surface()
        background = pygame.image.load(
            "assets/sprites/backgraund_win.jpg"
        ).convert()
        self.background = pygame.transform.scale(
            background,
            self.screen.get_size()
        )

    def event_cacher(self):
        """Handle clicks and keyboard input to continue or save the score."""
        self._update_score_eligibility()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if self.state == ScreenState.WIN_GAME:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.menu_rect.collidepoint(event.pos):
                        self.request_state_change(ScreenState.MENU)
                    elif self.Check_rect.collidepoint(event.pos):
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

    def _update_score_eligibility(self):
        if self._checked_score != self.score:
            self.can_add_score = is_high_score(self.score)
            self._checked_score = self.score

    def change_screen(self):
        """Return the destination screen after the chosen action."""
        target = self.consume_pending_state()
        if target is not None:
            return target
        return None

    def change_color_title(self):
        """Change the hovered text color for visual feedback."""
        mouse_pos = pygame.mouse.get_pos()

        self.menu_text = self.render_title(
            "Menu", self.menu_rect, (255, 255, 0), mouse_pos
        )
        self.new_score_text = self.render_title(
            "New Score", self.new_score_rect, (255, 255, 0), mouse_pos
        )
        check_color = (
            (135, 206, 235)
            if self.Check_rect.collidepoint(mouse_pos)
            else (255, 255, 255)
        )
        self.Check_text = self.lit.render(
            "Check top 10", True, check_color
        )

    def render(self):
        """Draw the win screen, buttons, and player name input."""
        self._update_score_eligibility()
        self.screen = pygame.display.get_surface()
        self.clear_screen()

        if self.state == ScreenState.WIN_GAME:
            self.screen.blit(self.background, (0, 0))
            self.change_color_title()
            self.screen.blit(self.win_text, self.win_rect)
            self.screen.blit(self.menu_text, self.menu_rect)
            self.screen.blit(self.Check_text, self.Check_rect)

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
