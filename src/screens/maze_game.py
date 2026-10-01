# from src.entitys.entity_base import Entity
# from src.entitys.sprite import Sprite
from src.screens.screen_base import ScreenBase
from src.entitys.man_pac import Man_Pac
from mazegenerator import MazeGenerator
from src import Surface, draw, pygame, Rect


class MazeScreen(ScreenBase):
    cell_size = 50
    wall_color = (255, 255, 255)
    wall_width = 1
    margin = 8

    def __init__(self):
        self.__maze_generator = MazeGenerator()
        self._generate_new_maze()
        self.pac_man = Man_Pac(
            start_point=self._board_to_pixel(
                    len(self.__maze) // 2,
                    len(self.__maze[0]) // 2
                )
        )

    def event_cacher(self):
        """
        Processes keyboard events
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_m]:
            self._generate_new_maze()

    def render(self) -> None:
        """
        Renders the maze.
        """
        print(self.pac_man.get_coord())
        self.__screen.blit(self.__maze_surface, (0, 0))
        self.__screen.blit(self.pac_man.get_sprite(), self.pac_man.get_coord())

    def clear_screen(self):

        self.__screen.fill("black")

    def change_screen(self):
        ...

    # Private functions
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
        surface_maze: Surface,
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

        draw.line(
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
            self.margin + (y * self.cell_size),
            self.margin + (x * self.cell_size))

    def _generate_new_maze(self) -> None:
        """
        Generate a screen with a new maze.
        """
        print("Generating maze...")
        self.__maze_generator.generate()
        self.__maze = self.__maze_generator.maze

        self.__screen = pygame.display.set_mode((
            len(self.__maze) * self.cell_size + self.margin * 2,
            len(self.__maze[0]) * self.cell_size + self.margin * 2
        ))
        self.__maze_surface = self._draw_maze(self.__maze).convert()
