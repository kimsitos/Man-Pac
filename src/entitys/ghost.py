from entitys.entity_base import Entity, Direction
from src.maze_class import Maze
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
        self._original_image = self.image.copy()
        self.return_path: list[Direction] = []

    def update(self, maze: Maze) -> None:
        self._wanted_dir = random.choice(list(Direction))

        if self.state == State.EATEABLE:
            if (pygame.time.get_ticks() - self._start_eatable
                    >= self._duration_eatable):
                self.make_inedible()

        elif self.is_returning_to_base():
            if not self.return_path:
                self.return_path = self._set_return_path(maze)
                print(self.return_path)
            
            if self._wanted_dir is None:
                self._wanted_dir = self.return_path.pop(0)
            if not self.return_path:
                self.make_inedible()


        super().update(maze)

    def is_eatable(self) -> bool:
        return self.state == State.EATEABLE

    def is_returning_to_base(self) -> bool:
        return self.state == State.RETURN_TO_BASE

    def make_eatable(self) -> None:
        self._start_eatable = pygame.time.get_ticks()
        self.image = self._original_image.copy()
        self.image.fill((255, 0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        self.state = State.EATEABLE

    def make_inedible(self) -> None:
        self.state = State.NONEATABLE
        self.image = self._original_image.copy()

    def get_point(self) -> int:
        return self.point_value

    def make_return_to_base(self):
        self.state = State.RETURN_TO_BASE
        self.image = self._original_image.copy()
        self.image.fill((0, 0, 255), special_flags=pygame.BLEND_RGBA_MULT)

    def _set_return_path(self, maze: Maze) -> list[Direction]:
        y, x = self.start_coord
        path = maze.shortest_path(
            self.get_coord(),
            (x, y)
            )
        return self._path_to_directions(path)

    @staticmethod
    def _path_to_directions(path: list[tuple[int, int]]) -> list[Direction]:
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
