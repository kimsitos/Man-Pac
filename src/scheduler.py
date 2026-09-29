from src.render import Render
import pygame
from mazegenerator import MazeGenerator
from src.entitys.entity_base import Entity
from enum import Enum


state = {
    "Menu": menu
}


class GameScheduler:
    def __init__(self) -> None:
        self.mazegen = MazeGenerator()
        self.man_pac = Entity(
            coord_x=250,
            coord_y=200,
            img_path="assets/sprites/Man-Pac.png"
        )
        self.render = Render()

    def run(self) -> None:
        """
        Run the game
        """
        self.running = True
        self.state = state
        while self.running:
            # Event catching
            self._event_cacher()

            self.render.clear_screen()
            self.state[estado].render
            estado = self.state[estado].changescreen()
            # For debug
            self.man_pac.move()

        pygame.quit()

    def _draw(self) -> None:
        """
        Draw the game scene depending on the state it is in
        """
        if self.state == State.MENU:
            self.render.render_menu()
        elif self.state == State.GAME:
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


class Pantalla()
    def event_cacher()

    def clear_screen()
    def render()