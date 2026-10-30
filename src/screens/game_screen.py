from src.entitys import PacMan, Ghost, Gumpac, SuperGumpac
from src.screens.screen_base import ScreenBase, ScreenState
from src.maze_class import Maze, cell_size
from src.parse_config_file import Parse_Config
from src import pygame


class GameScreen(ScreenBase):
    wall_color = (255, 255, 255)
    wall_width = 1
    margin = 8

    def __init__(self, config: Parse_Config):
        self.state = ScreenState.PLAY
        self.font = pygame.font.Font(None, 50)
        self.menu_text = self.font.render("Menu", True, (255, 255, 255))
        self.menu_rect = self.menu_text.get_rect(center=(1300, 50))
        self._maze = Maze(config.levels, seed=4)
        self.screen: pygame.Surface = pygame.display.get_surface()
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

        if len(self.pac_gums) <= 0:
            self.new_game()

        if keys[pygame.K_m]:
            for gumpac in self.pac_gums:
                gumpac.kill()

        self._check_collides()
        self.entitys.update(self._maze)
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
        if self.state != ScreenState.PLAY:
            return None

        self.change_color_title()
        self.screen.blit(self._maze.get_screen())
        self.screen.blit(self.menu_text, self.menu_rect)
        self.pac_gums.draw(self.screen)
        self.entitys.draw(self.screen)

    def change_screen(self):
        if self.state == ScreenState.PLAY:
            return None

        next_state = self.state.value
        self.state = ScreenState.PLAY
        return next_state

    def new_game(self):
        self._maze.generate_new_maze()
        self.pac_gums = self._create_pacgums(self._maze.get_maze())
        self.player.set_new_start_coord((
            ((len(self._maze.get_maze())) // 2) * cell_size,
            ((len(self._maze.get_maze()[0])) // 2) * cell_size
        ))

        maze = self._maze.get_maze()
        ghosts_pos = [
            (0 * cell_size, 0 * cell_size),
            (0 * cell_size, ((len(maze[0]) - 1) * cell_size)),
            ((len(maze) - 1) * cell_size, 0 * cell_size),
            ((len(maze) - 1) * cell_size, (len(maze[0]) - 1) * cell_size)
        ]

        for i, ghost in enumerate(self.ghosts):
            ghost.set_new_start_coord(ghosts_pos[i])
        self.state = ScreenState.PLAY

    def _check_collides(self):
        ghost_detection = pygame.sprite.spritecollide(
            self.player, self.ghosts,
            False,
            pygame.sprite.collide_circle)
        if ghost_detection:
            for ghost in ghost_detection:
                if ghost.is_eatable():
                    ghost.kill()
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
        import random

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
    

