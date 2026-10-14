from abc import ABC, abstractmethod
import pygame
from enum import Enum
from pathlib import Path
from src.maze_class import Maze, cell_size


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
        self.image: pygame.Surface = pygame.image.load(
            sprite_path
        )
        self.image = pygame.transform.scale(
            self.image,
            (cell_size - 1, cell_size - 1)
            )

        self.rect: pygame.Rect = self.image.get_rect()
        self.radius = self.rect.width // 2 - 4
        self.return_to_start()
        self._velocity = 2
        self._wanted_dir = Direction.NORTH
        self._direction: Direction = self._wanted_dir

    def move(self) -> None:
        """Moves the entity based on the assigned direction
        """
        if self._direction == Direction.NORTH:
            self.rect.y -= self._velocity
        elif self._direction == Direction.SOUTH:
            self.rect.y += self._velocity
        elif self._direction == Direction.EAST:
            self.rect.x += self._velocity
        elif self._direction == Direction.WEST:
            self.rect.x -= self._velocity

    def get_sprite(self) -> pygame.Surface:
        """Returns the sprite image

        Returns
        -------
        pygame.Surface
            The sprite image
        """
        return self.image

    def get_coord(self) -> tuple[int, int]:
        """Returns the coordinate where the sprite is 

        Returns
        -------
        tuple[int, int]
            The coordinate where the sprite is
        """
        return (self.rect.x, self.rect.y)

    def return_to_start(self):
        """Set the position so that it is in the starting position
        """
        self.rect.x, self.rect.y = self.start_coord

    @abstractmethod
    def update(self, maze: Maze) -> None:
        """Updates the direction the sprite moves

        Parameters
        ----------
        maze : Maze
            Maze grid. Each cell is a 4-bit mask (from 0 to 15)
            where each bit represents a wall
        """
        if maze.is_centered_in_cell(self.get_coord()):

            if not maze.intersect_wall(
                self.get_coord(),
                self._wanted_dir.value
            ):
                self._direction = self._wanted_dir
            if maze.intersect_wall(self.get_coord(), self._direction.value):
                return
        self.move()
