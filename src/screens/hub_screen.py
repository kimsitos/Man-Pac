import pygame


class Hubs:
    """Representa las stats debajo del juego."""

    def __init__(self, game_screen):
        self.game_screen = game_screen
        self.screen = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 50)
        self.score_text = self.font.render("score 0", True, (255, 255, 255))
        self.lives_text = self.font.render("lives 3", True, (255, 255, 255))
        self.time_text = self.font.render("Time ", True, (255, 255, 255))
        self.score_rect = self.score_text.get_rect()
        self.lives_rect = self.lives_text.get_rect()
        self.time_rect = self.time_text.get_rect()
        self._update_layout()

    def _update_layout(self):
        self.screen = pygame.display.get_surface()
        if self.screen is None:
            return

        texts = [self.score_text, self.lives_text, self.time_text]
        gap = 30
        total_width = sum(text.get_width() for text in texts) + gap * (len(texts) - 1)
        start_x = max((self.screen.get_width() - total_width) // 2, 20)
        y = self.screen.get_height() - 60

        current_x = start_x
        self.score_rect = self.score_text.get_rect(midleft=(current_x, y))
        current_x += self.score_text.get_width() + gap
        self.lives_rect = self.lives_text.get_rect(midleft=(current_x, y))
        current_x += self.lives_text.get_width() + gap
        self.time_rect = self.time_text.get_rect(midleft=(current_x, y))

    def get_required_width(self):
        texts = [self.score_text, self.lives_text, self.time_text]
        gap = 30
        return sum(text.get_width() for text in texts) + gap * (len(texts) - 1)

    def render(self):
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
        self._update_layout()

        self.screen.blit(self.score_text, self.score_rect)
        self.screen.blit(self.lives_text, self.lives_rect)
        self.screen.blit(self.time_text, self.time_rect)
