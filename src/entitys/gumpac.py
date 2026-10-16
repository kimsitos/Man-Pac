import pygame
from pathlib import Path
from src.maze_class import cell_size


class Gumpac(pygame.sprite.Sprite):
    image: pygame.Surface = pygame.image.load(
        "assets/sprites/Gumpac.png"
    )
    image = pygame.transform.scale(
        image,
        (cell_size // 2, cell_size // 2)
    )

    def __init__(self, position: tuple[int, int]):
        super().__init__()
        self.image = Gumpac.image
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.x, self.rect.y = position
        self.radius = self.rect.width // 2 - 4
        self.point_value = 50

    def get_point(self) -> int:
        return self.point_value


class SuperGumpac(Gumpac):
    point_value = 100

    def __init__(self, position: tuple[int, int]):
        super().__init__(position)
