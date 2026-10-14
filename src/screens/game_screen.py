from src.entitys import PacMan, Ghost
# from src.entitys.sprite import Sprite
from src.screens.screen_base import ScreenBase, ScreenState
from src.maze_class import Maze, cell_size
from src import pygame
import sys


class GameScreen(ScreenBase):
    wall_color = (255, 255, 255)
    wall_width = 1
    margin = 8

    def __init__(self):
        self.state = ScreenState.PLAY
        self.font = pygame.font.Font(None, 50)
        self.menu_text = self.font.render("Menu", True, (255, 255, 255))
        self.menu_rect = self.menu_text.get_rect(center=(1000, 50))
        self._maze = Maze()
        self._screen = pygame.display.set_mode(
            (self._maze.get_screen().get_size())
        )
        self._create_entitys()

    def event_cacher(self):
        """
        Processes keyboard events
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if self.state == ScreenState.PLAY:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.menu_rect.collidepoint(event.pos):
                        self.state = ScreenState.MENU_GAME

        keys = pygame.key.get_pressed()

        if keys[pygame.K_m]:
            self.new_game()

        self._check_collides()
        self._entitys.update(self._maze)

        return True

    def change_color_title(self):
        mouse_pos = pygame.mouse.get_pos()

        self.menu_text = self._render_title(
            "Menu", self.menu_rect, (255, 255, 0), mouse_pos
        )

    def render(self) -> None:
        """
        Renders the maze.
        """
        self.clear_screen()
        if self.state == ScreenState.PLAY:
            self.change_color_title()
            self._screen.blit(self._maze.get_screen())
            self._screen.blit(self.menu_text, self.menu_rect)
            self._entitys.draw(self._screen)

    def clear_screen(self) -> None:

        self._screen.fill("black")

    def change_screen(self):
        if self.state == ScreenState.PLAY:
            return None

        next_state = self.state.value
        self.state = ScreenState.PLAY
        return next_state

    def new_game(self):
        self._maze.generate_new_maze()
        self._screen = pygame.display.set_mode(
            (self._maze.get_screen().get_size())
        )
        for entity in self._entitys:
            entity.return_to_start()

    def _create_entitys(self) -> None:
        self._entitys: pygame.sprite.Group = pygame.sprite.Group()
        self.player = PacMan(
            (len(self._maze._generator.maze) // 2 * cell_size,
             len(self._maze._generator.maze[0]) // 2 * cell_size),
            "assets/sprites/Man-Pac.png"
        )
        self._entitys.add(self.player)

        maze = self._maze._generator.maze
        ghosts_pos = [
            (0 * cell_size, 0 * cell_size),
            (0 * cell_size, (len(maze) - 1) * cell_size),
            ((len(maze[0]) - 1) * cell_size, 0 * cell_size),
            ((len(maze[0]) - 1) * cell_size, (len(maze) - 1) * cell_size)
        ]

        self.ghost: pygame.sprite.Group = pygame.sprite.Group()
        self.ghost.add(Ghost(pos,
                             f"assets/sprites/Ghost{i}.png")
                       for i, pos in enumerate(ghosts_pos)
                       )
        del ghosts_pos

        self._entitys.add(self.ghost)

    def _check_collides(self):
        if pygame.sprite.spritecollide(
            self.player, self.ghost,
            False,
            pygame.sprite.collide_circle
        ):
            # provisional
            sys.exit()
