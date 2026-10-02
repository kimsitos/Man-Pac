from mazegenerator import MazeGenerator
import pygame


class Maze:
    cell_size = 50
    wall_color = (255, 255, 255)
    wall_width = 1

    def __init__(self, seed: int = 0):
        self._seed = seed
        self._generator = MazeGenerator(seed=self._seed)
        self._maze_screen = self._draw_maze(self._generator.maze)

    def generate_new_maze(self):
        self._generator.generate(self._seed)
        self._maze_screen = self._draw_maze(self._generator.maze)

    def get_screen(self) -> pygame.Surface:
        return self._maze_screen

    def _draw_maze(self, maze: list[list[int]]) -> pygame.Surface:
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

        surface_maze = pygame.Surface(
            (len(maze) * self.cell_size + 1,
             len(maze[0]) * self.cell_size + 1)
        )
        surface_maze.fill("black")
        for x in range(0, len(maze)):
            for y in range(0, len(maze[x])):
                value = maze[x][y]

                if value == 15:
                    pygame.draw.rect(
                        surface_maze,
                        "yellow",
                        pygame.Rect(
                            self._board_to_pixel(x, y),
                            (self.cell_size, self.cell_size)
                        )
                    )

                if value & E:
                    self._draw_wall(surface_maze, (x, y), (x, y+1))
                if value & N:
                    self._draw_wall(surface_maze, (x, y), (x+1, y))
                if value & S:
                    self._draw_wall(surface_maze, (x, y+1), (x+1, y+1))
                if value & O:
                    self._draw_wall(surface_maze, (x+1, y), (x+1, y+1))

        return surface_maze

    def _draw_wall(
        self,
        surface_maze: pygame.Surface,
        start: tuple[int, int],
            end: tuple[int, int]) -> None:
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
            surface_maze,
            self.wall_color,
            self._board_to_pixel(*start),
            self._board_to_pixel(*end),
            self.wall_width
        )

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
            y * self.cell_size,
            x * self.cell_size)

