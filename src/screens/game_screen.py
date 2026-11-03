from src.entitys import PacMan, Ghost, Gumpac, SuperGumpac
from src.screens.screen_base import ScreenBase, ScreenState
from src.screens.hub_screen import Hubs
from src.maze_class import Maze, cell_size
from src.parse_config_file import Config
import time
from src import pygame
import random


class GameScreen(ScreenBase):
    wall_color = (255, 255, 255)
    wall_width = 1
    margin = 8

    def __init__(self, config: Config):
        self.state = ScreenState.PLAY
        self.font = pygame.font.Font(None, 50)
        self._maze = Maze(config.levels, seed=4)
        self.screen: pygame.Surface = pygame.display.get_surface()
        self.hubs = Hubs(self)
        self.start_time = time.time()

        self._create_entitys()
        self._apply_config(config)

    def event_cacher(self):
        """
        Processes keyboard events
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        keys = pygame.key.get_pressed()

        if len(self.pac_gums) <= 0:
            self.new_game()

        if keys[pygame.K_m]:
            for gumpac in self.pac_gums:
                gumpac.kill()
        elif keys[pygame.K_ESCAPE]:
            self.state = ScreenState.MENU_GAME
        elif keys[pygame.K_1]:
            self.state = ScreenState.WIN_GAME
        elif keys[pygame.K_2]:
            self.state = ScreenState.LOST_GAME

        self._check_collides()
        self.entitys.update(self._maze)
        return True

    def render(self) -> None:
        """
        Renders the maze.
        """
        self.clear_screen()
        if self.state != ScreenState.PLAY:
            return None

        self.screen.blit(self._maze.get_screen())
        self.pac_gums.draw(self.screen)
        self.entitys.draw(self.screen)
        self.hubs.render()

    def change_screen(self):
        if self.state == ScreenState.PLAY:
            return None

        next_state = self.state.value
        self.state = ScreenState.PLAY
        return next_state

    def new_game(self):
        pygame.time.wait(200)
        try:
            self._maze.generate_new_maze()
            maze = self._maze.get_maze()
            self.pac_gums = self._create_pacgums(self._maze.get_maze())
            self.player.set_new_start_coord((
                ((len(self._maze.get_maze())) // 2) * cell_size,
                ((len(self._maze.get_maze()[0])) // 2) * cell_size
            ))
            self.player.return_to_start()

            ghosts_pos = [
                (0 * cell_size, 0 * cell_size),
                (0 * cell_size, ((len(maze[0]) - 1) * cell_size)),
                ((len(maze) - 1) * cell_size, 0 * cell_size),
                ((len(maze) - 1) * cell_size, (len(maze[0]) - 1) * cell_size)
            ]

            for i, ghost in enumerate(self.ghosts):
                ghost.set_new_start_coord(ghosts_pos[i])
                ghost.return_to_start()
            self.state = ScreenState.PLAY
        except StopIteration:
            self.state = ScreenState.WIN_GAME
        # breakpoint()

    def _check_collides(self):
        ghost_detection = pygame.sprite.spritecollide(
            self.player, self.ghosts,
            False,
            pygame.sprite.collide_circle)
        if ghost_detection:
            for ghost in ghost_detection:
                if ghost.is_eatable():
                    ghost.return_to_start()
                    self.player.set_score(ghost.get_point())
                else:
                    self.player.less_life()
                    for entity in self.entitys:
                        entity.return_to_start()
                    if self.player.is_dead():
                        self.state = ScreenState.LOST_GAME

        gumpac_detection = pygame.sprite.spritecollide(
            self.player, self.pac_gums,
            False,
            pygame.sprite.collide_circle
        )
        if gumpac_detection:
            gumpac = gumpac_detection[0]
            self.player.set_score(gumpac.point_value)
            if isinstance(gumpac, SuperGumpac):
                for ghost in self.ghosts:
                    ghost.make_eatable()

            gumpac.kill()
        if len(self.pac_gums) == 0:
            self.new_game()

    def _apply_config(self, config: Config) -> None:
        random.seed(config.seed)
        self.time_max = config.level_max_time
        PacMan.lives = config.lives
        Gumpac.point_value = config.points_per_pacgum
        SuperGumpac.point_value = config.points_per_super_pacgum
        Ghost.point_value = config.points_per_ghost

    # Creation of Game Objects
    def _create_entitys(self) -> None:
        self.entitys: pygame.sprite.Group = pygame.sprite.Group()

        player_start_pos = (
            ((len(self._maze.get_maze())) // 2) * cell_size,
            ((len(self._maze.get_maze()[0])) // 2) * cell_size
        )

        self.player = PacMan(
            player_start_pos,
            "assets/sprites/Man-Pac.png"
        )

        self.ghosts = self._create_ghosts(self._maze.get_maze())
        self.pac_gums = self._create_pacgums(self._maze.get_maze())

        self.entitys.add(self.player)
        self.entitys.add(self.ghosts)

    @staticmethod
    def _create_ghosts(maze: list[list[int]]) -> pygame.sprite.Group:
        ghosts_pos = [
            (0 * cell_size, 0 * cell_size),
            (0 * cell_size, ((len(maze[0]) - 1) * cell_size)),
            ((len(maze) - 1) * cell_size, 0 * cell_size),
            ((len(maze) - 1) * cell_size, (len(maze[0]) - 1) * cell_size)
        ]

        ghost: pygame.sprite.Group = pygame.sprite.Group()
        ghost.add(Ghost(pos,
                        f"assets/sprites/Ghost{i}.png")
                  for i, pos in enumerate(ghosts_pos)
                  )

        return ghost

    @staticmethod
    def _create_pacgums(maze: list[list[int]]) -> pygame.sprite.Group:

        pac_gums: pygame.sprite.Group = pygame.sprite.Group()
        pac_gums.add(Gumpac(
            (
                (x * cell_size) + (cell_size // 4),
                (y * cell_size) + (cell_size // 4)
            ))
            for y in range(len(maze))
            for x in range(len(maze[y]))
            if maze[y][x] != 15
        )

        for _ in range(4):
            gum = random.choice(pac_gums.sprites())
            pac_gums.remove(gum)
            supergum = SuperGumpac(gum.rect.topleft)
            pac_gums.add(supergum)

        return pac_gums

    
    def manage_time(self, time_max):
        time_f = time.time()

        if time_f - self.start_time >= time_max:
            self.player.less_life()
            for entity in self.entitys:
                entity.return_to_start()
            self.start_time = time.time()
            if self.player.is_dead():
                self.state = ScreenState.LOST_GAME

        return int((time_f - self.start_time) - time_max)

    def get_stats(self):
        time_f = self.manage_time(self.time_max)
        return {
            "score": self.player.get_score(),
            "lives": self.player.get_lives(),
            "time": time_f,
        }
