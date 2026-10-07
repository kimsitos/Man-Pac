from abc import ABC, abstractmethod
import pygame
from enum import Enum
from pathlib import Path


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
        if not Path(sprite_path).exists():
            raise ValueError(f"Can't access sprite file {sprite_path}")
        self.image = pygame.Surface([39,39])
        self.image.fill("orange")
        self.rect = self.image.get_rect()
        self.return_to_start()
        self._velocity = 1
        self._wanted_dir = Direction.NORTH
        self._direction = self._wanted_dir

    def move(self, maze) -> None:

        if maze.is_centered_in_cell(self.get_coord()):

            if not maze.intersect_wall(
                self.get_coord(),
                self._wanted_dir.value
            ):
                self._direction = self._wanted_dir
            if m
            aze.intersect_wall(self.get_coord(), self._direction.value):
                return

        if self._direction == Direction.NORTH:
            self.rect.centery -= self._velocity
        elif self._direction == Direction.SOUTH:
            self.rect.centery += self._velocity
        elif self._direction == Direction.EAST:
            self.rect.centerx += self._velocity
        elif self._direction == Direction.WEST:
            self.rect.centerx -= self._velocity

    def get_sprite(self) -> pygame.Surface:
        return self.image

    def get_coord(self) -> tuple[int, int]:
        return (self.rect.centerx, self.rect.centery)

    def return_to_start(self):
        self.rect.centerx, self.rect.centery = self.start_coord

    @abstractmethod
    def update(self):
        pass
