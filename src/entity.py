from src import BaseModel, Surface
from enum import Enum
from pathlib import Path
from typing import Any
import pygame


class Move(Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


class Entity(BaseModel):
    #state: Enum
    movement: Move = "LEFT"
    coord_x: int
    coord_y: int
    img_path: Path

    def model_post_init(self, _: Any) -> None:
        if not self.img_path.is_file():
            raise FileNotFoundError()
        
        self._sprite = pygame.image.load(self.img_path)
        self._sprite = pygame.transform.scale(self._sprite, (45, 45))
    
    def get_coord(self) -> tuple[int, int]:
        return (self.coord_y + 2 + 8, self.coord_x + 2 + 8)
    
    def get_sprite(self) -> Surface:
        return self._sprite
