from src.render import Render
import pygame
from mazegenerator import MazeGenerator
from src.entity import Entity
from enum import Enum


class State(Enum):
    MENU = 1
    GAME = 2
    LEADERBOARD = 3


class GameScheduler:
    def __init__(self) -> None:
        self.mazegen = MazeGenerator()

    def generate_maze(self) -> list[list[int]]:
        self.mazegen.generate()
        return self.mazegen.maze

    def run(self):
        self.render = Render(self.generate_maze())
        running = True
        self.man_pac = Entity(
            coord_x=250,
            coord_y=200,
            img_path="assets/Man-Pac.png"
        )

        self.state = State.GAME
        while running:
            # Event catching
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.render.clear_screen()
            self._draw()

        pygame.quit()

    def _draw(self) -> None:
        if self.state == State.MENU:
            self.render.render_menu()
        if self.state == State.GAME:
            self.render.render_maze(self.generate_maze(), self.man_pac)

