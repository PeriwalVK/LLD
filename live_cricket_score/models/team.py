from __future__ import annotations

from typing import List

from live_cricket_score.models.player import Player


class Team:
    """Cricket team aggregate with an ordered squad list."""

    def __init__(self, team_id: str, name: str, squad: List[Player]):
        if len(squad) < 2:
            raise ValueError("Team needs at least two players")
        self.team_id = team_id
        self.name = name
        self.squad = list(squad)

    def __repr__(self) -> str:
        return f"Team({self.team_id!r}, {self.name!r})"
