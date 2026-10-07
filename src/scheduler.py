import pygame
from enum import Enum

from src.screens.menu import Menu
from src.screens.game_screen import GameScreen
from src.screens.high_score import High_score


class ScreenState(Enum):
    MENU = "MENU"
    PLAY = "PLAY"
    HIGH_SCORE = "HIGH_SCORE"


class GameScheduler:
    def __init__(self):
        pygame.init()
        self.current_state = ScreenState.MENU.value
        self.screens = {
            ScreenState.MENU.value: Menu(),
            ScreenState.PLAY.value: GameScreen(),
            ScreenState.HIGH_SCORE.value: High_score(),
        }
        self.running = True

    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            screen = self.screens[self.current_state]

            if not screen.event_cacher():
                self.running = False
                break
            next_state = screen.change_screen()
            if next_state is not None and next_state in self.screens:
                self.current_state = next_state
                screen = self.screens[self.current_state]

            screen.render()
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
