from entitys.entity_base import Entity, Direction
from src.maze_class import Maze
import random
import pygame
from enum import Enum, auto


class State(Enum):
    NORMAL = auto()
    EATEABLE = auto()


class Ghost(Entity):
    point_value = 200
    def __init__(
        self,
        start_coord: tuple[int, int],
            sprite_path: str):
        super().__init__(start_coord, sprite_path)
        self._duration_eatable = 50 * 200
        self._start_eatable = pygame.time.get_ticks()
        self.state = State.NORMAL

    def update(self, maze: Maze) -> None:
        self._wanted_dir = random.choice(list(Direction))

        if self.state == State.EATEABLE:
            print(pygame.time.get_ticks() - self._start_eatable)
            if pygame.time.get_ticks() - self._start_eatable >= self._duration_eatable:
                self.state = State.NORMAL
                print("non Eatable")
       
        super().update(maze)

    def is_eatable(self) -> bool:
        return self.state == State.EATEABLE

    def make_eatable(self) -> None:
        self._start_eatable = pygame.time.get_ticks()
        self.state = State.EATEABLE
        print("IM EATABLE NOW")

    def get_point(self) -> int:
        return self.point_value
