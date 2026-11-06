import pygame


class Hubs:
    """Representa las stats debajo del juego."""

    def __init__(self, game_screen):
        self.game_screen = game_screen
        self.screen = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 50)
        self.spacing = 70
        self._update_layout()

    def _update_layout(self):
        width, height = self.screen.get_size()
        self.score_text = self.font.render("score 0", True, (255, 255, 255))
        self.score_rect = self.score_text.get_rect(center=(width * 0.15, height - 40))

        self.lives_text = self.font.render("lives 3", True, (255, 255, 255))
        self.lives_rect = self.lives_text.get_rect(center=(width * 0.5, height - 40))

        self.time_text = self.font.render("Time ", True, (255, 255, 255))
        self.time_rect = self.time_text.get_rect(center=(width * 0.85, height - 40))

    def get_required_width(self):
        return (
            self.score_text.get_width()
            + self.spacing
            + self.lives_text.get_width()
            + self.spacing
            + self.time_text.get_width()
        )

    def render(self):
        self.screen = pygame.display.get_surface()
        self._update_layout()

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

        total_width = self.get_required_width()
        left_margin = max(40, (self.screen.get_width() - total_width) // 2)

        self.score_rect = self.score_text.get_rect(center=(left_margin + self.score_text.get_width() / 2, self.screen.get_height() - 40))
        self.lives_rect = self.lives_text.get_rect(center=(left_margin + self.score_text.get_width() + self.spacing + self.lives_text.get_width() / 2, self.screen.get_height() - 40))
        self.time_rect = self.time_text.get_rect(center=(left_margin + self.score_text.get_width() + self.spacing + self.lives_text.get_width() + self.spacing + self.time_text.get_width() / 2, self.screen.get_height() - 40))

        self.screen.blit(self.score_text, self.score_rect)
        self.screen.blit(self.lives_text, self.lives_rect)
        self.screen.blit(self.time_text, self.time_rect)
