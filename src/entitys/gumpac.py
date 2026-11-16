import pygame
from src.maze_class import cell_size
import sys


def load_sprite(path: str) -> pygame.Surface:
    try:
        image = pygame.image.load(path)
        return pygame.transform.scale(
            image,
            (cell_size // 2, cell_size // 2)
        )
    except FileNotFoundError as error:
        print("\033[91mFile not found Error:\033[0m", error)
        sys.exit(1)


class Gumpac(pygame.sprite.Sprite):
    image = load_sprite("assets/sprites/Gumpac.png")
    point_value = 50

    def __init__(self, position: tuple[int, int]):
        super().__init__()
        self.image = type(self).image
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.x, self.rect.y = position
        self.radius = self.rect.width // 2 - 4

    def get_point(self) -> int:
        return self.point_value


class SuperGumpac(Gumpac):
    point_value = 100
    image = load_sprite("assets/sprites/SuperGumpac.png")

    def __init__(self, position: tuple[int, int]):
        super().__init__(position)
