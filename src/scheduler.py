from src.render import Render
import pygame
from mazegenerator import MazeGenerator
from src.entity import Entity


class GameScheduler:
    def run(self):
        running = True
        mazegen = MazeGenerator()
        render = Render(mazegen.maze)
        man_pac = Entity(
            coord_x=250,
            coord_y=200,
            img_path="assets/Man-Pac.png"
        )

        state = "GAME"
        while running:
            # Event catching
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            render.clear_screen()
            if state == "GAME":
                render.render_maze(mazegen.maze, man_pac)

        pygame.quit()
