from src.entity import Entity
from src.sprite import Sprite
from . import Surface, draw, pygame, Rect


class MazeScreen():
    cell_size = 50
    wall_color = (255, 255, 250)

    def __init__(self, maze: list[list[int]], man_pac: Entity) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((
            self.cell_size * len(maze) + 5,
            self.cell_size * len(maze[0]) + 5
        ))
        self._maze_surface = self._draw_maze(maze)
        self.man_pac = man_pac

    def run(self) -> None:
        self.clock = pygame.time.Clock()
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            self.screen.blit(self._maze_surface)
            self.clock.tick(60)
            pygame.display.flip()

        pygame.quit()

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
            (len(maze) * self.cell_size,
             len(maze[0]) * self.cell_size)
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
                        self._board_to_pixel(x, y + 1)
                    )

                if value & N:
                    draw.line(
                        surface_maze,
                        self.wall_color,
                        self._board_to_pixel(x, y),
                        self._board_to_pixel(x+1, y)
                    )
                if value & S:
                    draw.line(
                        surface_maze,
                        self.wall_color,
                        self._board_to_pixel(x, y + 1),
                        self._board_to_pixel(x+1, y + 1)
                    )
                if value & O:
                    draw.line(
                        surface_maze,
                        self.wall_color,
                        self._board_to_pixel(x + 1, y),
                        self._board_to_pixel(x + 1, y + 1)
                    )

        return surface_maze

        def draw_sprite(self, sprite: Sprite) -> None:
            """Draw the sprite on the screen

            Parameters
            ----------
            sprite : Sprite
                class that contains a surface with the image to be
                illustrated and the coordinates where it can be taught
            """
            y, x = sprite.get_coord()
            self.screen.blit(sprite.get_sprite(), (y, x))

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