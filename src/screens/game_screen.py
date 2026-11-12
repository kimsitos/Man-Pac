from src.entitys import PacMan, Ghost, Gumpac, SuperGumpac
from src.screens.screen_base import ScreenBase, ScreenState
from src.screens.hub_screen import Hubs
from src.maze_class import Maze, cell_size
from src.cheat_mode import Cheat_Mode
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
        self.cheat = Cheat_Mode()
        self.font = pygame.font.Font(None, 50)
        self._maze = Maze(config.levels, config.seed)
        self.screen: pygame.Surface = pygame.display.get_surface()
        self.hubs = Hubs(self)
        self.start_time = time.time()

        self._create_entitys()
        self.config = config
        self._apply_config(config)

    def event_cacher(self):
        """
        Processes keyboard events
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_m and self.cheat.enable:
                    print("Level skipped")
                    for gumpac in self.pac_gums:
                        gumpac.kill()
            self.cheat.catch_cheat_keys(event)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            self.state = ScreenState.MENU_GAME
        elif keys[pygame.K_1]:
            self.state = ScreenState.WIN_GAME
        elif keys[pygame.K_2]:
            self.state = ScreenState.LOST_GAME

        self._check_collides()
        self.player.update(self._maze)
        if not (self.cheat.enable and self.cheat.ghost_freeze):
            dist_map = self._maze.dist_map(self.player.get_coord())
            self.ghosts.update(self._maze, dist_map=dist_map)
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

    def _resize_to_maze(self):
        """Adjust the window to fit the maze, leaving room for the HUDv"""
        maze = self._maze.get_maze()
        maze_width = len(maze[0]) * cell_size
        maze_height = len(maze) * cell_size
        hub_width = self.hubs.get_required_width()
        min_width = max(maze_width, hub_width + (self.margin * 4))
        min_height = maze_height + 140

        new_size = (max(min_width, 500), max(min_height, 500))
        current_size = pygame.display.get_surface().get_size()
        if current_size != new_size:
            pygame.display.set_mode(new_size)

        self.screen = pygame.display.get_surface()
        self.hubs._update_layout()

    def new_game(self):
        self._maze = Maze(self.config.levels, self.config.seed)
        self._create_entitys()

    def new_level(self):
        pygame.time.wait(200)
        try:
            self._maze.generate_new_maze()
            maze = self._maze.get_maze()
            self.pac_gums = self._create_pacgums(self._maze.get_maze())

            row, col = len(maze) // 2, len(maze[0]) // 2
            print(row, col)
            while maze[row][col] == 15:
                col -= 1
            self.player.set_new_start_coord(
                (row * cell_size, col * cell_size)
            )
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

            self._resize_to_maze()
            self.state = ScreenState.PLAY
        except StopIteration:
            self.new_game()
            self.state = ScreenState.WIN_GAME

    def _check_collides(self):
        self._ghost_colides()

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
                    if not ghost.is_returning_to_base():
                        ghost.make_eatable()

            gumpac.kill()

        if len(self.pac_gums) <= 0:
            self.new_level()

    def _ghost_colides(self):
        ghost_detection = pygame.sprite.spritecollide(
            self.player, self.ghosts,
            False,
            pygame.sprite.collide_circle)

        if ghost_detection:
            for ghost in ghost_detection:
                if ghost.is_returning_to_base():
                    continue

                if ghost.is_eatable():
                    ghost.make_return_to_base()
                    self.player.set_score(ghost.get_point())
                    pygame.time.wait(150)

                elif not (self.cheat.enable and self.cheat.invencibility):
                    self.player.less_life()
                    for entity in self.entitys:
                        entity.return_to_start()
                        if isinstance(entity, PacMan):
                            continue
                        entity.make_inedible()
                    if self.player.is_dead():
                        self.state = ScreenState.LOST_GAME

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
        maze = self._maze.get_maze()

        row, col = len(maze) // 2, len(maze[0]) // 2
        print(row, col)
        while maze[row][col] == 15:
            row -= 1

        self.player = PacMan(
            (row * cell_size, col * cell_size),
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
        super_gumpac_pos = [
            (0, 0),
            (0, ((len(maze[0]) - 1))),
            ((len(maze) - 1), 0),
            ((len(maze) - 1), (len(maze[0]) - 1))
        ]
        pac_gums: pygame.sprite.Group = pygame.sprite.Group()
        for y in range(len(maze)):
            for x in range(len(maze[y])):
                if maze[y][x] != 15:
                    if (x, y) in super_gumpac_pos:
                        pac_gums.add(SuperGumpac(
                            (
                                (x * cell_size) + (cell_size // 4),
                                (y * cell_size) + (cell_size // 4)
                            ))
                        )
                    else:
                        pac_gums.add(Gumpac(
                            (
                                (x * cell_size) + (cell_size // 4),
                                (y * cell_size) + (cell_size // 4)
                            ))
                        )

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
