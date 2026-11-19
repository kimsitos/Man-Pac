import pygame
import sys


class Cheat_Mode:
    invencibility: bool = False
    ghost_freeze: bool = False

    def __init__(self) -> None:
        self.enable = (True if "--cheat_mode" in (argv.lower()
                       for argv in sys.argv)
                       else False)

        if self.enable:
            print("Cheat Mode enabled")
            print("M - Skip level")
            print("G - Activate/Deactivate Freeze ghosts")
            print("I - Activate/Deactivate invencibility")

    def catch_cheat_keys(self, event: pygame.event.Event) -> None:
        """
        process the events for the cheat modes

        Parameters
        ----------
        event : pygame.event.Event
            Pygame event to inspect for cheat key releases
        """
        if not self.enable:
            return
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_g:
                self.ghost_freeze = not self.ghost_freeze
                print("Ghost Freeze:",
                      "Enable" if self.ghost_freeze
                      else "Desabled")

            elif event.key == pygame.K_i:
                self.invencibility = not self.invencibility
                print("Invencibility:",
                      "Enable" if self.invencibility
                      else "Desabled")
