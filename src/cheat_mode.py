import pygame
import sys


class Cheat_Mode:
    invencibility: bool = False
    ghost_freeze: bool = False

    def __init__(self):
        self.enable = (True if "--cheat_mode" in (argv.lower()
                       for argv in sys.argv)
                       else False)


    def catch_cheat_keys(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_g:
                self.ghost_freeze = not self.ghost_freeze
            elif event.key == pygame.K_i:
                self.invencibility = not self.invencibility
