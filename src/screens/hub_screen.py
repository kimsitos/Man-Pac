import pygame


class Hubs:
    """Representa las stats debajo del juego."""

    def __init__(self, game_screen):
        self.game_screen = game_screen
        self.screen = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 50)
        self.score_text = self.font.render("score 0", True, (255, 255, 255))
        self.score_rect = self.score_text.get_rect(center=(100, 950))

        self.lives_text = self.font.render("lives 3", True, (255, 255, 255))
        self.lives_rect = self.lives_text.get_rect(center=(600 // 2, 950))

        self.time_text = self.font.render("Time ", True, (255, 255, 255))
        self.time_rect = self.time_text.get_rect(center=(900 // 2, 950))

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

        self.screen.blit(self.score_text, self.score_rect)
        self.screen.blit(self.lives_text, self.lives_rect)
        self.screen.blit(self.time_text, self.time_rect)
