from src.render import Render
import pygame
from mazegenerator import MazeGenerator
from src.entity import Entity


class GameScheduler:
    mazegen = MazeGenerator()

    def generate_maze(self) -> list[list[int]]:
        return self.mazegen.generate_maze().maze

    def run(self):
        running = True
        render = Render(self.generate_maze())
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
                render.render_maze(self.generate_maze(), man_pac)

        pygame.quit()
