from src import BaseModel
from enum import Enum
from typing import cast, List, Dict, Any
from pathlib import Path
import json
import pygame

from src.screens.screen_base import ScreenBase


class StateMachine(Enum):
    """Maquina de estados de high score"""
    MENU = "MENU"
    HIGH_SCORE = "HIGH_SCORE"


class Player(BaseModel):
    """Representa un jugador para registros."""
    name: str
    scored: int


class High_score(ScreenBase):
    """pantalla de high score"""
    state = StateMachine.HIGH_SCORE

    def __init__(self):
        self.players = load_players("high_scores.json")
        self.font = pygame.font.Font(None, 50)
        self.title_font = pygame.font.Font(None, 80)
        self.menu_text = self.font.render("MENU", True, (255, 255, 255))
        self.menu_rect = self.menu_text.get_rect(center=(1200 // 2, 930))
        self.screen = pygame.display.set_mode((1200, 1000))

    def event_cacher(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if self.state == StateMachine.HIGH_SCORE:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.menu_rect.collidepoint(event.pos):
                        self.state = StateMachine.MENU
        return True

    def change_screen(self) -> str:
        return self.state

    def clear_screen(self) -> None:
        self.screen.fill((0, 0, 0))

    def change_color_title(self):
        mouse_pos = pygame.mouse.get_pos()

        self.menu_text = self._render_title(
            "Menu", self.menu_rect, (255, 255, 0), mouse_pos
        )

    def render_high_scores(self):
        title = self.title_font.render(
            "TOP 10 SCORES",
            True,
            (255, 255, 0)
        )

        self.screen.blit(title, (350, 50))

        start_y = 180

        for index, player in enumerate(self.players):
            text = self.font.render(
                f"{index + 1}. {player.name:<10} {player.scored}",
                True,
                (255, 255, 255)
            )

            self.screen.blit(
                text,
                (250, start_y + index * 70)
            )

    def _render_title(
        self,
        text: str,
        rect: Any,
        hover_color: tuple[int, int, int],
        mouse_pos: tuple[int, int],
    ) -> Any:
        color = (
            hover_color
            if rect.collidepoint(mouse_pos)
            else (255, 255, 255)
        )
        return self.font.render(text, True, color)

    def render(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            running = self.event_cacher()
            if not running:
                break
            self.clear_screen()

            if self.state == StateMachine.HIGH_SCORE:
                self.render_high_scores()
                self.change_color_title()
                self.screen.blit(self.menu_text, self.menu_rect)
            elif self.state == StateMachine.MENU:
                self.change_screen()
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()


def new_record(new: Player):
    """Insert new score."""

    players = load_players("high_scores.json")
    players.append(new)

    players.sort(
        key=lambda player: player.scored,
        reverse=True
    )

    _write_json(players[:10])


def load_players(path: str) -> list[Player]:
    """Load and validate players."""

    data = _load_json(path)

    list_players = [
        Player.model_validate(item)
        for item in data
    ]
    if len(list_players) > 10:
        raise ValueError(
            "There can only be 10 players on the high scores list."
        )
    elif len(list_players) < 0:
        return "There are not scores"
    return list_players


def _load_json(path: str) -> list[dict]:
    """Load a JSON file."""

    try:
        with open(path, encoding="utf-8") as file:
            data = json.load(file)
            return cast(List[Dict[str, Any]], data)

    except FileNotFoundError as exc:

        raise RuntimeError(
            f"File not found: {path}"
        ) from exc

    except json.JSONDecodeError as exc:

        raise RuntimeError(
            f"Invalid JSON: {path}"
        ) from exc


def _write_json(players: list[Player]):
    """ Write generated function calls to JSON."""

    output_path = Path("high_scores.json")

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output_path.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            [
                player.model_dump()
                for player in players
            ],
            file,
            indent=4,
            ensure_ascii=False,
        )


if __name__ == "__main__":
    pygame.init()
    high = High_score()
    high.render()
