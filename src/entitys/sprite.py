from pathlib import Path
from src import pygame, Surface, BaseModel
from typing import Any


class Sprite(BaseModel):
    coord_x: int
    coord_y: int
    img_path: Path

    def model_post_init(self, _: Any) -> None:
        if not self.img_path.is_file():
            raise FileNotFoundError()

        self._sprite = pygame.image.load(self.img_path)
        self._sprite = pygame.transform.scale(self._sprite, (45, 45))

    def get_coord(self) -> tuple[int, int]:
        return (self.coord_y, self.coord_x)

    def get_sprite(self) -> Surface:
        return self._sprite
