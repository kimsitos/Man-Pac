from src import BaseModel
from enum import Enum
from typing import cast, List, Dict, Any
from pathlib import Path
import json
import pygame


class StateMachine(Enum):
    BACK = "BACK"
    HIGH_SCORE = "HIGH_SCORE"


class Player(BaseModel):
    """Representa un jugador para registros."""
    name: str
    scored: int


class High_score():
    state: Any = StateMachine.HIGH_SCORE

    def render(self):

        font = pygame.font.Font(None, 100)
        back_text = font.render("JUGAR", True, (255, 255, 255))
        back_rect = back_text.get_rect(center=(1200 // 2, 900))
        screen = pygame.display.set_mode((1200, 1000))
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill((0, 0, 0))
            if self.state == StateMachine.HIGH_SCORE:

                screen.blit(back_text, back_rect)
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
