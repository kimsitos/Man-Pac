from entitys.entity_base import Entity, Direction
import pygame


class PacMan(Entity):
    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self._direction = Direction.NORTH
        elif keys[pygame.K_s]:
            self._direction = Direction.SOUTH
        elif keys[pygame.K_d]:
            self._direction = Direction.EAST
        elif keys[pygame.K_a]:
            self._direction = Direction.WEST
