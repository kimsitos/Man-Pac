from src.entitys.man_pac import PacMan
# from src.entitys.sprite import Sprite
from src.screens.screen_base import ScreenBase
from src.maze_class import Maze
from src import pygame


class GameScreen(ScreenBase):
    cell_size = 50
    wall_color = (255, 255, 255)
    wall_width = 1
    margin = 8

    def __init__(self):
        self._maze = Maze()
        self.entidad = PacMan(
            (len(self._maze._generator.maze) // 2 * self._maze.cell_size,
             len(self._maze._generator.maze[0]) // 2 * self._maze.cell_size),
            "assets/sprites/Man-Pac.png"
        )
        self._screen = pygame.display.set_mode(
            (self._maze.get_screen().get_size())
        )

    def event_cacher(self):
        """
        Processes keyboard events
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_m]:
            self._maze.generate_new_maze()
            self._screen = pygame.display.set_mode(
                (self._maze.get_screen().get_size())
            )
            self.entidad.return_to_start()
        self.entidad.update()
        self.entidad.move(self._maze)
        return True

    def render(self) -> None:
        """
        Renders the maze.
        """
        self.clear_screen()
        self._screen.blit(self._maze.get_screen())
        self._screen.blit(self.entidad.get_sprite(), self.entidad.get_coord())

    def clear_screen(self):

        self._screen.fill("black")

    def change_screen(self):
        return None
