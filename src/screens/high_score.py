from src import BaseModel
from typing import cast, List, Dict, Any
from pathlib import Path
import json
import pygame

from src.screens.screen_base import ScreenBase, ScreenState


class Player(BaseModel):
    """Represents a player record for the leaderboard."""
    name: str
    scored: int


class High_score(ScreenBase):
    """Screen with the top scores leaderboard."""

    def __init__(self) -> None:
        """Load the background and prepare the score list."""
        super().__init__()
        self.state = ScreenState.HIGH_SCORE
        self.players = list[Player]
        self.font = pygame.font.Font(None, 60)
        self.title_font = pygame.font.Font(None, 80)
        self.menu_text = self.font.render("Menu", True, (255, 255, 255))
        self.menu_rect = self.menu_text.get_rect(center=(1200 // 2, 950))
        self.screen = pygame.display.get_surface()
        background = pygame.image.load(
            "assets/sprites/background_high_score.jpg"
        ).convert()
        self.background = pygame.transform.scale(
            background,
            self.screen.get_size()
        )

    def event_cacher(self) -> Any:
        """Handle clicks on the back-to-menu button."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if self.state == ScreenState.HIGH_SCORE:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.menu_rect.collidepoint(event.pos):
                        self.request_state_change(ScreenState.MENU)
        return True

    def change_screen(self) -> Any:
        """Return the screen change queued by the menu click."""
        target = self.consume_pending_state()
        if target is not None:
            return target
        return None

    def change_color_title(self) -> None:
        """Highlight the menu button while the mouse is over it."""
        mouse_pos = pygame.mouse.get_pos()

        self.menu_text = self.render_title(
            "Menu", self.menu_rect, (255, 255, 0), mouse_pos
        )

    def render_high_scores(self) -> None:
        """Draw the ordered ranking of the best results."""
        title = self.title_font.render(
            "TOP 10 SCORES",
            True,
            (255, 255, 0)
        )
        self.players = load_players("high_scores.json")
        self.screen.blit(title, (350, 50))

        for index, player in enumerate(self.players):

            if index == 0:
                color = (255, 215, 0)
            elif index == 1:
                color = (192, 192, 192)
            elif index == 2:
                color = (205, 127, 50)
            else:
                color = (255, 255, 255)

            pos_text = self.font.render(
                f"{index + 1}.",
                True,
                color
            )

            name_text = self.font.render(
                player.name,
                True,
                color
            )

            score_text = self.font.render(
                str(player.scored),
                True,
                color
            )

            y = 180 + index * 70

            self.screen.blit(pos_text, (195, y))
            self.screen.blit(name_text, (280, y))
            self.screen.blit(score_text, (850, y))

    def render(self) -> None:
        """Draw the background, leaderboard, and return button."""
        self.screen = pygame.display.get_surface()
        self.clear_screen()

        if self.state == ScreenState.HIGH_SCORE:
            self.screen.blit(self.background, (0, 0))
            self.render_high_scores()
            self.change_color_title()
            self.screen.blit(self.menu_text, self.menu_rect)


def new_record(new: Player) -> None:
    """Insert a new score."""

    players = load_players("high_scores.json")
    players.append(new)

    players.sort(
        key=lambda player: player.scored,
        reverse=True
    )

    _write_json(players[:10])


def is_high_score(score: int) -> bool:
    """Return whether a score beats the current lowest leaderboard entry."""
    players = load_players("high_scores.json")
    return not players or score > min(player.scored for player in players)


def load_players(path: str) -> list[Player]:
    """Load and validate player records."""

    data = _load_json(path)

    list_players = [
        Player.model_validate(item)
        for item in data
    ]
    if len(list_players) > 10:
        raise ValueError(
            "There can only be 10 players on the high scores list."
        )
    if not list_players:
        return []
    return list_players


def _load_json(path: str) -> list[dict]:
    """Load a JSON file from disk."""

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


def _write_json(players: list[Player]) -> None:
    """Write the leaderboard to the JSON file."""

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
