from abc import ABC, abstractmethod
import pygame
from enum import Enum


class Direction(Enum):
    NORTH = "North"
    WEST = "West"
    SOUTH = "South"
    EAST = "East"


class Entity(ABC, pygame.sprite.Sprite):

    def __init__(
        self,
        start_coord: tuple[int, int],
            sprite_path: str):

        pygame.sprite.Sprite.__init__(self)
        self.start_coord = start_coord
        self.return_to_start()
        self.image = pygame.image.load(sprite_path)
        self.image = pygame.transform.scale(self.image, (48, 48))

        
        self._velocity = 1
        self._direction = Direction.WEST

    def move(self) -> None:
        if self._direction == Direction.NORTH:
            self._y -= self._velocity
        elif self._direction == Direction.SOUTH:
            self._y += self._velocity
        elif self._direction == Direction.EAST:
            self._x += self._velocity
        elif self._direction == Direction.WEST:
            self._x -= self._velocity

    def get_sprite(self) -> pygame.Surface:
        return self.image

    def get_coord(self) -> tuple[int, int]:
        return (self._x, self._y)
    
    def return_to_start(self):
        self._x, self._y = self.start_coord

    @abstractmethod
    def update(self):
        pass