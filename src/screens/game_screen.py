from src.entitys.man_pac import PacMan
# from src.entitys.sprite import Sprite
from src.screens.screen_base import ScreenBase
from src.maze_class import Maze, cell_size
from src import pygame


class GameScreen(ScreenBase):
    wall_color = (255, 255, 255)
    wall_width = 1
    margin = 8

    def __init__(self):
        self._maze = Maze()
        self.player = PacMan(
            (len(self._maze._generator.maze) // 2 * cell_size,
             len(self._maze._generator.maze[0]) // 2 * cell_size),
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
            self.player.return_to_start()
        self.player.update(self._maze)
        return True

    def render(self) -> None:
        """
        Renders the maze.
        """
        self.clear_screen()
        self._screen.blit(self._maze.get_screen())
        self._screen.blit(self.player.get_sprite(), self.player.get_coord())

    def clear_screen(self):

        self._screen.fill("black")

    def change_screen(self):
        return None
