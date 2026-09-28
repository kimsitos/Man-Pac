from src import BaseModel, Surface
from src.sprite import Sprite
from enum import Enum
from pathlib import Path
from typing import Any
import pygame


class Move(Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


class Entity(Sprite):
    #state: Enum
    movement: Move = Move.LEFT
