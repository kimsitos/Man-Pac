from entitys.entity_base import Entity, Direction
from src.maze_class import Maze
import random
import pygame
from enum import Enum, auto


class State(Enum):
    NONEATABLE = auto()
    EATEABLE = auto()


class Ghost(Entity):
    point_value = 200

    def __init__(
        self,
        start_coord: tuple[int, int],
            sprite_path: str):
        super().__init__(start_coord, sprite_path)
        self._duration_eatable = 50 * 100
        self._start_eatable = pygame.time.get_ticks()
        self.state = State.NONEATABLE
        self._original_image = self.image.copy()

    def update(self, maze: Maze) -> None:
        self._wanted_dir = random.choice(list(Direction))

        if self.state == State.EATEABLE:
            if (pygame.time.get_ticks() - self._start_eatable
                    >= self._duration_eatable):
                self.make_eatable()

        super().update(maze)

    def is_eatable(self) -> bool:
        return self.state == State.EATEABLE

    def make_eatable(self) -> None:
        self._start_eatable = pygame.time.get_ticks()
        self.image.fill((255, 0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        self.state = State.EATEABLE

    def make_inedible(self) -> None:
        self.state = State.NONEATABLE
        self.image = self._original_image.copy()

    def get_point(self) -> int:
        return self.point_value
