from pygame import Rect, Surface, draw


class Render():
    cell_size = 50
    wall_color = (255, 255, 255)
    margin = 8

    def __init__(self, maze: list[list[int]]):
        self._maze_surface = self._maze_draw(maze)

    def get_maze_surface(self) -> Surface:
        """
        Returns the maze surface

        Returns
        -------
        Surface
           The surface where the labyrinth is drawn
        """
        return self._maze_surface

    def _maze_draw(self, maze: list[list[int]]) -> Surface:
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
