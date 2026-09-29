from src.entitys.sprite import Sprite
from enum import Enum


class Movement(Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


class Entity(Sprite):
    velocity: int = 5
    movement: Movement = Movement.LEFT

    def move(self) -> None:
        if self.movement == Movement.LEFT:
            self.coord_y += self.velocity
        if self.movement == Movement.DOWN:
            self.coord_x += self.velocity
        if self.movement == Movement.RIGHT:
            self.coord_y -= self.velocity
        if self.movement == Movement.UP:
            self.coord_x -= self.velocity
