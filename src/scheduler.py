import pygame
from src.screens.screen_base import ScreenState
from src.screens.menu import Menu
from src.screens.menu_game import Menu_Game
from src.screens.game_screen import GameScreen
from src.screens.high_score import High_score
from src.screens.win_game import Win_Game
from src.screens.lost_game import Lost_Game
from src.parse_config_file import parse_config_file

import sys


class GameScheduler:
    def __init__(self):
        pygame.init()
        pygame.display.set_mode((1200, 1000))
        self.current_state = ScreenState.MENU.value
        self.game_screen = GameScreen(parse_config_file(sys.argv[1]))
        self.screens = {
            ScreenState.MENU.value: Menu(),
            ScreenState.MENU_GAME.value: Menu_Game(),
            ScreenState.PLAY.value: self.game_screen,
            ScreenState.HIGH_SCORE.value: High_score(),
            ScreenState.LOST_GAME.value: Lost_Game(),
            ScreenState.WIN_GAME.value: Win_Game()
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
                if (
                    next_state == ScreenState.MENU.value
                    and self.current_state
                    in {
                        ScreenState.MENU_GAME.value,
                        ScreenState.LOST_GAME.value,
                    }
                ):
                    self.game_screen.new_game()
                self.current_state = next_state
                screen = self.screens[self.current_state]

            screen.render()
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
