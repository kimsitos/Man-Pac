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
    def __init__(self) -> None:
        """
            Initialize the game loop and the default screen state.
        """
        pygame.init()
        self.default_screen_size = (1200, 1000)
        pygame.display.set_mode(self.default_screen_size)
        self.current_state = ScreenState.MENU.value
        self.previous_state = None

        try:
            self.game_screen: GameScreen = GameScreen(
                parse_config_file(sys.argv[1])
                )
        except IndexError:
            print("\033[91mFile not found Error:\033[0m", "Insert config file")
            sys.exit(1)

        self.screens = {
            ScreenState.MENU.value: Menu(),
            ScreenState.MENU_GAME.value: Menu_Game(),
            ScreenState.PLAY.value: self.game_screen,
            ScreenState.HIGH_SCORE.value: High_score(),
            ScreenState.LOST_GAME.value: Lost_Game(),
            ScreenState.WIN_GAME.value: Win_Game()
        }
        self.running = True

    def _sync_display_size(self) -> None:
        """
        Resize only when a screen transition actually changes state.
        """
        if self.current_state == self.previous_state:
            return

        if self.current_state == ScreenState.PLAY.value:
            self.game_screen._resize_to_maze()
        else:
            pygame.display.set_mode(self.default_screen_size)

        self.previous_state = self.current_state

    def run(self) -> None:
        """
        Main loop: process input, apply transitions, and render frames.
        """
        clock = pygame.time.Clock()

        while self.running:
            self._sync_display_size()
            screen = self.screens[self.current_state]

            if not screen.event_cacher():
                self.running = False
                break
            next_state = screen.change_screen()
            if next_state is not None and next_state in self.screens:
                if next_state in {
                    ScreenState.WIN_GAME.value,
                    ScreenState.LOST_GAME.value,
                }:
                    self.screens[next_state].score = (
                        self.game_screen.player.get_score()
                    )
                if (
                    next_state == ScreenState.PLAY.value
                    and self.current_state == ScreenState.MENU.value
                ):
                    self.game_screen.start_time
                if (
                    next_state == ScreenState.MENU.value
                    and self.current_state
                    in {
                        ScreenState.MENU_GAME.value,
                        ScreenState.LOST_GAME.value,
                        ScreenState.WIN_GAME.value,
                        ScreenState.HIGH_SCORE.value,
                    }
                ):
                    self.game_screen.new_game()
                self.current_state = next_state
                screen = self.screens[self.current_state]

            screen.render()
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
