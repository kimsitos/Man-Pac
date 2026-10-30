from mazegenerator import MazeGenerator
import pygame
from src.parse_config_file import Level


cell_size = 50


class Maze:
    wall_color = (255, 255, 255)
    wall_width = 1

    def __init__(self, levels: list[Level], seed: int = 0):
        self.seed = seed
        self.levels = self._get_new_level(levels)
        self._mask_walls = {
            "North": 1,
            "West": 8,
            "South": 4,
            "East": 2
        }
        self.generate_new_maze()

    def generate_new_maze(self) -> None:
        """Generates a new maze based on
        the previously given seed
        """
        level = next(self.levels)
        self._generator = MazeGenerator(size=level, seed=self.seed)
        self._draw_maze(self._generator.maze)

    def get_maze(self) -> list[list[int]]:
        """Returns the maze grid. Each cell is a 4-bit mask (from 0 to 15)
            where each bit represents a wall

        Returns
        -------
        list[list[int]]
            Maze grid. Each cell is a 4-bit mask (from 0 to 15)
            where each bit represents a wall
        """
        return self._generator.maze

    def get_screen(self) -> pygame.Surface:
        """Returns the surface on which the maze is drawn

        Returns
        -------
        pygame.Surface
            The surface on which the maze is drawn
        """
        return self._maze_screen

    def is_centered_in_cell(self, pos: tuple[int, int]) -> bool:
        """Checks that the given coordinates are
        centered in a cell on the x and y axis

        Parameters
        ----------
        pos : tuple[int, int]
            Coordinates of the entity.
            Format: (x, y)

        Returns
        -------
        bool
            True if it is centered on the x and y axes
            of the cell in which it is positioned.
            False if not
        """
        px, py = pos
        if (px % cell_size != 0) or (py % cell_size != 0):
            return False
        return True

    def intersect_wall(self, pos: tuple[int, int], direction: str) -> bool:
        """checks that an entity does not intersect
        a wall based on its coordinates

        Parameters
        ----------
        pos : tuple[int, int]
            Coordinates of the entity.
            Format: (x, y)
        direction : str
            String of the cardinal direction to
            which you want to move the entity

        Returns
        -------
        bool
            True if it intersects a wall, False if it does not intersect a wall
        """
        py, px = pos
        row = py // cell_size
        col = px // cell_size
        cell = self._generator.maze[col][row]
        return (cell & self._mask_walls[direction]) != 0

    @staticmethod
    def _get_new_level(levels: list[Level]):
        for level in levels:
            yield (level.width, level.height)

    def _draw_maze(self, maze: list[list[int]]) -> None:
        """
        Create the surface where the drawn maze is

        Parameters
        ----------
        maze : list[list[int]]
            Maze grid. Each cell is a 4-bit mask (from 0 to 15)
            where each bit represents a wall
        """
        self._maze_screen = pygame.Surface(
            (len(maze[0]) * cell_size + 1,
             len(maze) * cell_size + 1)
        )
        self._maze_screen.fill("black")
        for y in range(0, len(maze)):
            for x in range(0, len(maze[y])):
                value = maze[y][x]

                px = x * cell_size
                py = y * cell_size

                if value == 15:
                    pygame.draw.rect(
                        self._maze_screen,
                        "yellow",
                        pygame.Rect(
                            (px, py),
                            (cell_size, cell_size)
                        )
                    )

                if value & self._mask_walls["East"]:
                    self._draw_wall(
                        (px + cell_size, py),
                        (px + cell_size, py + cell_size)
                    )
                if value & self._mask_walls["North"]:
                    self._draw_wall((px, py), (px + cell_size, py))
                if value & self._mask_walls["South"]:
                    self._draw_wall(
                        (px, py + cell_size),
                        (px + cell_size, py + cell_size)
                    )
                if value & self._mask_walls["West"]:
                    self._draw_wall((px, py), (px, py + cell_size))

    def _draw_wall(self, start: tuple[int, int], end: tuple[int, int]) -> None:
        """
        Draw a line on the given screen.

        Parameters
        ----------
        surface_maze : Surface
            Surface on which to draw the line
        start : tuple[int, int]
            Line start point
        end : tuple[int, int]
            Line end point
        """

        pygame.draw.line(
            self._maze_screen,
            self.wall_color,
            start,
            end,
            self.wall_width
        )
