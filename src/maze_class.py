from mazegenerator import MazeGenerator
import pygame


class Maze:
    cell_size = 50
    wall_color = (255, 255, 255)
    wall_width = 1

    def __init__(self, seed: int = 0):
        self._seed = seed
        self._generator = MazeGenerator(seed=self._seed)
        self._mask_walls = {
            "North": 1,
            "West": 8,
            "South": 4,
            "East": 2
        }
        self._draw_maze(self._generator.maze)

    def generate_new_maze(self):
        self._generator.generate(self._seed)
        self._maze_screen = self._draw_maze(self._generator.maze)

    def get_screen(self) -> pygame.Surface:
        return self._maze_screen

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
            (len(maze) * self.cell_size + 1,
             len(maze[0]) * self.cell_size + 1)
        )
        self._maze_screen.fill("black")
        for y in range(0, len(maze)):
            for x in range(0, len(maze[y])):
                value = maze[y][x]

                px = x * self.cell_size
                py = y * self.cell_size

                if value == 15:
                    pygame.draw.rect(
                        self._maze_screen,
                        "yellow",
                        pygame.Rect(
                            (px, py),
                            (self.cell_size, self.cell_size)
                        )
                    )

                if value & self._mask_walls["East"]:
                    self._draw_wall(
                        (px + self.cell_size, py),
                        (px + self.cell_size, py + self.cell_size)
                    )
                if value & self._mask_walls["North"]:
                    self._draw_wall((px, py), (px + self.cell_size, py))
                if value & self._mask_walls["South"]:
                    self._draw_wall(
                        (px, py + self.cell_size),
                        (px + self.cell_size, py + self.cell_size)
                    )
                if value & self._mask_walls["West"]:
                    self._draw_wall((px, py), (px, py + self.cell_size))

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
