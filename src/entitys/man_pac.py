from entitys.entity_base import Entity, Direction
from src.maze_class import Maze
import pygame


class PacMan(Entity):
    lives = 3

    def __init__(
        self,
        start_coord: tuple[int, int],
            sprite_path: str):
        self.score = 0
        super().__init__(start_coord, sprite_path)

    def update(self, maze: Maze) -> None:
        """Updates the direction the sprite moves

        Parameters
        ----------
        maze : Maze
            Maze grid. Each cell is a 4-bit mask (from 0 to 15)
            where each bit represents a wall
        """
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self._wanted_dir = Direction.NORTH
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self._wanted_dir = Direction.SOUTH
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self._wanted_dir = Direction.EAST
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self._wanted_dir = Direction.WEST

        super().update(maze)

    def set_score(self, points: int) -> None:
        """adds the point value to the total score

        Parameters
        ----------
        points : int
            point value to add
        """
        if points <= 0:
            return
        self.score += points

    def get_score(self) -> int:
        """Return the actual score

        Returns
        -------
        int
            actual score
        """
        return self.score

    def is_dead(self) -> bool:
        """Checks if man_pac is dead

        Returns
        -------
        bool
            True if manpac is dead. False otherwise
        """
        if self.lives <= 0:
            return True
        return False

    def less_life(self) -> bool:
        """Reduce by 1 the lives that man_pac has

        Returns
        -------
        bool
            True if manpac is dead. False otherwise
        """
        if self.is_dead():
            return True
        self.lives -= 1
        return False

    def get_lives(self) -> int:
        """Return the lives that man_pac has

        Returns
        -------
        int
            lives that man_pac has
        """
        return self.lives
