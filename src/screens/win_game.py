from screen_base import ScreenBase, ScreenState
import pygame

class Win_Game(ScreenBase):
    """pantalla de victoria del juego"""

    def __init__(self):
        self.state = ScreenState.WIN_GAME
        self.font = pygame.font.Font(None, 120)
        self.win_text = self.font.render("You Win!", True, (255, 255, 255))
        self.win_rect = self.win_text.get_rect(center=(600, 690))
        self.menu_text = self.font.render("Menu", True, (255, 255, 255))
        self.menu_rect = self.menu_text.get_rect(center=(600, 600))
        self.screen = pygame.display.get_surface()

    def event_cacher(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if self.state == ScreenState.WIN_GAME:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.menu_rect.collidepoint(event.pos):
                        self.state = ScreenState.MENU
        return True

    def change_screen(self):
        if self.state == ScreenState.WIN_GAME:
            return None

        next_state = self.state.value
        self.state = ScreenState.WIN_GAME
        return next_state

    def change_color_title(self):
        mouse_pos = pygame.mouse.get_pos()

        self.menu_text = self._render_title(
            "Menu", self.menu_rect, (255, 255, 0), mouse_pos
        )

    def render(self):
        self.clear_screen()

        if self.state == ScreenState.WIN_GAME:
            self.change_color_title()
            self.screen.blit(self.win_text, self.win_rect)
            self.screen.blit(self.menu_text, self.menu_rect)


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    win_game_screen = Win_Game()

    running = True
    while running:
        running = win_game_screen.event_cacher()
        win_game_screen.render()
        pygame.display.flip()

    pygame.quit()