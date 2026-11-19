from mazegenerator import MazeGenerator
import pygame
import sys
from heapq import heappop, heappush
from src.parse_config_file import Level
from typing import Iterator


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
        maze: list[list[int]] = self._generator.maze
        return maze

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
        return bool((cell & self._mask_walls[direction]) != 0)

    def dist_map(self, start: tuple[int, int]) -> list[list[int]]:
        """Build a minimum-distance map from a starting pixel position

        Parameters
        ----------
        start : tuple[int, int]
            start point in pixels (row, col)

        Returns
        -------
        list[list[int]]
            2D grid of shortest step distances from the starting cell to each
            cell in the maze.
        """
        x, y = start
        distance, _ = self._explore((y // cell_size, x // cell_size))
        return distance

    def shortest_path(
        self,
        start: tuple[int, int],
        end: tuple[int, int]
    ) -> list[tuple[int, int]]:
        """Generate the shortest path from the start coordinate
        inside the maze to the end

        Parameters
        ----------
        start : tuple[int, int]
            pixel position on the maze
        end : tuple[int, int]
            pixel position on the maze

        Returns
        -------
        list[tuple[int, int]]
            tuple list of the cells to go through to get to the end
        """

        psx, psy = start
        pex, pey = end

        start = (psy // cell_size, psx // cell_size)
        end = (pey // cell_size, pex // cell_size)

        if start == end:
            return []

        distance, previous = self._explore(start)

        if distance[end[0]][end[1]] == sys.maxsize:
            return []
        path: list[tuple[int, int]] = []
        current: tuple[int, int] | None = end

        while current is not None:
            path.append(current)
            row, col = current
            current = previous[row][col]

        path.reverse()

        return path

    def get_neightbour(
        self,
        cell_pos: tuple[int, int]
    ) -> list[tuple[int, int]]:
        """returns neighboring cells that are connected

        Parameters
        ----------
        cell_pos : tuple[int, int]
            cell you want to get your neighbors

        Returns
        -------
        list[tuple[int, int]]
            neighbor cells that are connected
        """

        row, col = cell_pos

        maze = self.get_maze()
        cell_value = maze[row][col]

        neighbours = []

        if not (cell_value & self._mask_walls["North"]):
            neighbours.append((row - 1, col))
        if not (cell_value & self._mask_walls["South"]):
            neighbours.append((row + 1, col))
        if not (cell_value & self._mask_walls["West"]):
            neighbours.append((row, col - 1))
        if not (cell_value & self._mask_walls["East"]):
            neighbours.append((row, col + 1))

        return neighbours

    def _explore(self, start: tuple[int, int]
                 ) -> tuple[list[list[int]],
                            list[list[tuple[int, int] | None]]]:
        """Compute shortest distances and predecessors from a starting cell.

        Traverses the maze returned using a min-heap priority
        queue (Dijkstra's algorithm) with unit step cost between neighboring
        cells.

        Parameters
        ----------
        start : tuple[int, int]
            (row, column) coordinates of the starting cell.

        Returns
        -------
        tuple[list[list[int]], list[list[tuple[int, int] | None]]]
            `(distance, previous)`` tuple where:
            - ``distance`` is a 2D integer grid of shortest path lengths from
              ``start`` (``sys.maxsize`` if unreachable).
            - ``previous`` is a 2D grid holding the ``(row, column)``
              predecessor cell along the shortest path, or ``None`` if unset.
        """

        maze = self.get_maze()
        rows = len(maze)
        cols = len(maze[0])
        distance = [
            [sys.maxsize for _ in range(cols)]
            for _ in range(rows)
        ]
        previous: list[list[tuple[int, int] | None]] = [
            [None for _ in range(cols)]
            for _ in range(rows)
        ]

        distance[start[0]][start[1]] = 0
        visited = set()
        min_heap = [(0, start)]

        while min_heap:
            current_cost, current = heappop(min_heap)
            if current in visited:
                continue

            visited.add(current)

            for neighbour in self.get_neightbour(current):
                if neighbour in visited:
                    continue

                nr, nc = neighbour
                cost = current_cost + 1

                if cost < distance[nr][nc]:
                    distance[nr][nc] = cost
                    previous[nr][nc] = current
                    heappush(min_heap, (cost, neighbour))

        return distance, previous

    @staticmethod
    def _get_new_level(levels: list[Level]) -> Iterator[tuple[int, int]]:
        """Yield dimensions for each level from a list of level objects

        Parameters
        ----------
        levels : list[Level]
            list of Level class, where where the width and
            height of the level are saved

        Yields
        ------
        Iterator[tuple[int, int]]
           Tuple (width, height) representing each level's dimensions
        """
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
