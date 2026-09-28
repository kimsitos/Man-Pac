from mazegenerator import MazeGenerator
from random import randint
from src.man_pac import main
from src.render import Render
from src.menu import Menu 
from src.entity import Entity
import pygame

def main():
    labernto = MazeGenerator()
    for row in labernto.maze:
        print(row)
    
        
    man_pac = Entity(
        coord_x=0,
        coord_y=0,
        img_path="assets/Man-Pac.png"
    )
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((1280, 1000))
    clock = pygame.time.Clock()
    running = True
    render = Render(labernto.maze)
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("purple")
        screen.blit(render.get_maze_surface())
        screen.blit(man_pac.get_sprite(), man_pac.get_coord())

        # RENDER YOUR GAME HERE
        

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()

if __name__ == "__main__":
    main()
    #menu = Menu()
    #menu.render_menu()

