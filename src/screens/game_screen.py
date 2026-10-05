from src.entitys import PacMan
# from src.entitys.sprite import Sprite
from src.screens.screen_base import ScreenBase
from src.maze_class import Maze
from src import Surface, draw, pygame, Rect


class GameScreen(ScreenBase):
    cell_size = 50
    wall_color = (255, 255, 255)
    wall_width = 1
    margin = 8

    def __init__(self):
        self.entidad = PacMan(
            (100, 80),
            "assets/sprites/Man-Pac.png"
        )
        self._maze = Maze()
        self._screen = pygame.display.set_mode(
            (self._maze.get_screen().get_size())
        )

    def event_cacher(self):
        """
        Processes keyboard events
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_m]:
            self._maze.generate_new_maze()
            self._screen = pygame.display.set_mode(
                (self._maze.get_screen().get_size())
            )
            self.entidad.return_to_start()
        self.entidad.update()
        self.entidad.move()

    def render(self) -> None:
        """
        Renders the maze.
        """
        self._screen.blit(self._maze.get_screen())
        self._screen.blit(self.entidad.get_sprite(), self.entidad.get_coord())

    def clear_screen(self):

        self._screen.fill("black")

    def change_screen(self):
        ...