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
        self.man_pac = Entity(
            coord_x=250,
            coord_y=200,
            img_path="assets/Man-Pac.png"
        )
        self.render = Render()

    def run(self) -> None:
        """
        Run the game
        """
        self.running = True
        self.state = State.GAME
        while self.running:
            # Event catching
            self._event_cacher()

            self.render.clear_screen()
            self._draw()
            # For debug
            self.man_pac.move()

        pygame.quit()

    def _draw(self) -> None:
        """
        Draw the game scene depending on the state it is in
        """
        if self.state == State.MENU:
            self.render.render_menu()
        if self.state == State.GAME:
            self.render.render_maze(self.generate_maze(), self.man_pac)

    def _event_cacher(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def generate_maze(self) -> list[list[int]]:
        """
        Generate a maze with the mazegen library

        Returns
        -------
        list[list[int]]
            Maze grid. Each cell is a 4-bit mask (from 0 to 15)
            where each bit represents a wall
        """
        self.mazegen.generate()
        return self.mazegen.maze
