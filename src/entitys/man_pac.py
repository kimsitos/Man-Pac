from entitys.entity_base import Entity, Direction
import pygame


class PacMan(Entity):
    def update(self) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self._wanted_dir = Direction.NORTH
        elif keys[pygame.K_s]:
            self._wanted_dir = Direction.SOUTH
        elif keys[pygame.K_d]:
            self._wanted_dir = Direction.EAST
        elif keys[pygame.K_a]:
            self._wanted_dir = Direction.WEST