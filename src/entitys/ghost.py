from entitys.entity_base import Entity, Direction
from src.maze_class import Maze
import random


class Ghost(Entity):
    def __init__(
        self,
        start_coord: tuple[int, int],
            sprite_path: str):
        super().__init__(start_coord, sprite_path)
        self._point_value = 200

    def update(self, maze: Maze) -> None:
        self._wanted_dir = random.choice(list(Direction))

        super().update(maze)
