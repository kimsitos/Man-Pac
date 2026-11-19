from entitys.entity_base import Entity, Direction
from src.maze_class import Maze, cell_size
import random
import pygame
from enum import Enum, auto


class State(Enum):
    NONEATABLE = auto()
    EATEABLE = auto()
    RETURN_TO_BASE = auto()


class Ghost(Entity):
    point_value = 200

    def __init__(
        self,
        start_coord: tuple[int, int],
            sprite_path: str):
        super().__init__(start_coord, sprite_path)
        self._duration_eatable = 5000
        self._start_eatable = pygame.time.get_ticks()
        self.state = State.NONEATABLE
        self._original_image: pygame.Surface = self.image.copy()
        self.return_path: list[Direction] = []

    def update(self, maze: Maze, dist_map: list[list[int]]) -> None:
        """Updates the direction the sprite moves
        based on the state of the ghost

        Parameters
        ----------
        maze : Maze
            Maze grid. Each cell is a 4-bit mask (from 0 to 15)
            where each bit represents a wall
        """
        if (maze.is_centered_in_cell(self.get_coord())
                and not self.is_returning_to_base()):
            self._wanted_dir = random.choice(
                [self.next_move(maze, dist_map),
                 random.choice(list(Direction))]
            )

        if self.state == State.EATEABLE:
            if (pygame.time.get_ticks() - self._start_eatable
                    >= self._duration_eatable):
                self.make_inedible()

        elif self.is_returning_to_base():
            if not self.return_path:
                self.return_path = self._set_return_path(maze)

            if maze.is_centered_in_cell(self.get_coord()):
                try:
                    self._wanted_dir = self.return_path.pop(0)
                except IndexError:
                    self._wanted_dir = random.choice(list(Direction))
                    self.make_inedible()

        super().update(maze)

    def next_move(self, maze: Maze, dist_map: list[list[int]]) -> Direction:
        """processes the information from the dist_map to
        take the direction depending on the state you are in

        Parameters
        ----------
        maze : Maze
            Maze grid. Each cell is a 4-bit mask (from 0 to 15)
            where each bit represents a wall
        dist_map : list[list[int]]
            2D grid of shortest step distances from the starting cell to each
            cell in the maze.

        Returns
        -------
        Direction
            Direction where the ghost moves
        """
        def dist(cell: tuple[int, int]) -> int:
            """Return the dist value of a cell

            Parameters
            ----------
            cell : tuple[int, int]
                cell on the 2d map

            Returns
            -------
            int
                dist value
            """
            return dist_map[cell[0]][cell[1]]

        x, y = self.get_coord()
        row, col = y // cell_size, x // cell_size
        neightbour_cells = maze.get_neightbour((row, col))

        maze_map = maze.get_maze()
        object_cell = maze_map[row][col]
        if self.state == State.EATEABLE:
            object_cell = max(neightbour_cells, key=dist)
        elif self.state == State.NONEATABLE:
            object_cell = min(neightbour_cells, key=dist)

        return self._path_to_directions([(row, col), object_cell])[0]

    def is_eatable(self) -> bool:
        """Return whether the ghost is currently in the eatable state

        Returns
        -------
        bool
            True if the state is EATABLE. False otherwise
        """
        return self.state == State.EATEABLE

    def is_returning_to_base(self) -> bool:
        """Return whether the ghost is currently in the return_to_base state

        Returns
        -------
        bool
            True if the state is RETURN_TO_BASE. False otherwise
        """
        return self.state == State.RETURN_TO_BASE

    def make_eatable(self) -> None:
        """It makes the ghost edible, along with its characteristics"""
        self._start_eatable = pygame.time.get_ticks()
        self.image = self._original_image.copy()
        self.image.fill((255, 0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        self.state = State.EATEABLE

    def make_inedible(self) -> None:
        """It makes the ghost inedible, along with its characteristics"""
        self.state = State.NONEATABLE
        self.image = self._original_image.copy()

    def get_point(self) -> int:
        """returns its score value

        Returns
        -------
        int
            score value
        """
        return self.point_value

    def make_return_to_base(self) -> None:
        """It makes the ghost return_to_base, along with its characteristics"""
        self.state = State.RETURN_TO_BASE
        self.image = self._original_image.copy()
        self.image.fill((100, 50, 255), special_flags=pygame.BLEND_RGBA_MULT)

    def _set_return_path(self, maze: Maze) -> list[Direction]:
        """Return a list of directions to the base of the ghost

        Parameters
        ----------
        maze : Maze
            Maze grid. Each cell is a 4-bit mask (from 0 to 15)
            where each bit represents a wall

        Returns
        -------
        list[Direction]
            List of Directions that the ghost must follow to return to the bse
        """
        y, x = self.start_coord
        path = maze.shortest_path(
            self.get_coord(),
            (x, y)
            )
        return self._path_to_directions(path)

    @staticmethod
    def _path_to_directions(path: list[tuple[int, int]]) -> list[Direction]:
        """transforms a list of neighboring cells into a list of Directions

        Parameters
        ----------
        path : list[tuple[int, int]]
            list of neighboring cells to travel to reach x point

        Returns
        -------
        list[Direction]
            list of Directions to go to reach x point
        """
        directions = []
        direction_map = {
            (-1, 0): Direction.NORTH,
            (1, 0): Direction.SOUTH,
            (0, -1): Direction.WEST,
            (0, 1): Direction.EAST
        }
        for i in range(1, len(path)):
            previous = path[i - 1]
            current = path[i]

            delta = (
                current[0] - previous[0],
                current[1] - previous[1]
            )

            directions.append(direction_map[delta])

        return directions
