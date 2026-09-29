import pygame
from src.screens.menu import Menu
from src.entitys.entity_base import Entity
from src.screens.maze_game import MazeScreen


class GameScheduler:
    def __init__(self) -> None:
        pac_man = Entity(img_path="assets/sprites/Man-Pac.png")
        self.screens = {
            "GAME": MazeScreen()
        }

    def run(self) -> None:
        """
        Run the game
        """
        screen = "GAME"
        clock = pygame.time.Clock()
        self.running = True
        while self.running:
            # Event catching
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.screens[screen].event_cacher()

            self.screens[screen].clear_screen()
            self.screens[screen].render()

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
