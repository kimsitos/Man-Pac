import pygame
import sys


class Cheat_Mode:
    invencibility: bool = False

    def __init__(self):
        self.enable = (True if "--cheat_mode" in (argv.lower()
                       for argv in sys.argv)
                       else False)

        print(self.enable)
