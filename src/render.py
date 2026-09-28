import pygame
from pygame import Rect, Surface, draw
from src.entity import Entity
from src.sprite import Sprite


class Render():
    cell_size = 50
    wall_color = (255, 255, 255)
    wall_width = 2
    margin = 8

    def __init__(self, maze: list[list[int]]):
        pygame.init()
        self.screen = pygame.display.set_mode((
            len(maze) * self.cell_size + self.margin * 2,
            len(maze[0]) * self.cell_size + self.margin * 2
            ))
        self.clock = pygame.time.Clock()
        self._maze_surface = self._draw_maze(maze)

    def render_maze(self, maze: list[list[int]], pac_man: Entity) -> None:

        self.screen.blit(self._maze_surface)
        self.draw_sprite(pac_man)

        pygame.display.flip()
        self.clock.tick(60)

    def render_menu(self) -> None:
        ...

    def render_leaderboard(self) -> None:
        ...

    def clear_screen(self) -> None:
        self.screen.fill("purple")

    def draw_sprite(self, sprite: Sprite) -> None:
        y, x = sprite.get_coord()
        y += self.wall_width + self.margin
        x += self.wall_width + self.margin
        self.screen.blit(sprite.get_sprite(), (y, x))

    def get_maze_surface(self) -> Surface:
        """
        Returns the maze surface

        Returns
        -------
        Surface
           The surface where the labyrinth is drawn
        """
        return self._maze_surface

    def _draw_maze(self, maze: list[list[int]]) -> Surface:
        """
        Create the surface where the drawn maze is

        Parameters
        ----------
        maze : list[list[int]]
            Maze grid. Each cell is a 4-bit mask (from 0 to 15)
            where each bit represents a wall

        Returns
        -------
        Surface
            The surface where the labyrinth is drawn
        """
        N, O, S, E = 8, 4, 2, 1

        surface_maze = Surface(
            (self.margin * 2 + len(maze) * self.cell_size,
             self.margin * 2 + len(maze[0]) * self.cell_size)
            )
        surface_maze.fill("black")
        for x in range(0, len(maze)):
            for y in range(0, len(maze[x])):
                value = maze[x][y]

                if value == 15:
                    draw.rect(
                        surface_maze,
                        "yellow",
                        Rect(
                            self._board_to_pixel(x, y),
                            (self.cell_size, self.cell_size)
                        )
                    )

                if value & E:
                    draw.line(
                        surface_maze,
                        self.wall_color,
                        self._board_to_pixel(x, y),
                        self._board_to_pixel(x, y + 1),
                        self.wall_width
                    )

                if value & N:
                    draw.line(
                        surface_maze,
                        self.wall_color,
                        self._board_to_pixel(x, y),
                        self._board_to_pixel(x+1, y),
                        self.wall_width
                    )
                if value & S:
                    draw.line(
                        surface_maze,
                        self.wall_color,
                        self._board_to_pixel(x, y + 1),
                        self._board_to_pixel(x+1, y + 1),
                        self.wall_width
                    )
                if value & O:
                    draw.line(
                        surface_maze,
                        self.wall_color,
                        self._board_to_pixel(x + 1, y),
                        self._board_to_pixel(x + 1, y + 1),
                        self.wall_width
                    )

        return surface_maze

    def _board_to_pixel(self, x: int, y: int) -> tuple[int, int]:
        """
        Returns the position of the two-dimensional array to
        the corresponding pixel

        Parameters
        ----------
        x : int
            x position of the two-dimensional array
        y : int
            y position of the two-dimensional array

        Returns
        -------
        tuple[int, int]
            corresponding coordinates for the surface
        """
        return (
            self.margin + y * self.cell_size,
            self.margin + x * self.cell_size)
