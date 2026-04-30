from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Set

from live_cricket_score.models.player import Player
from live_cricket_score.models.team import Team


@dataclass
class BattingLineup:
    """
    Tracks active batters and dismissed players for an innings.
    """

    players: List[Player]
    striker_index: int = 0
    non_striker_index: int = 1
    dismissed_ids: Set[str] = field(default_factory=set)

    def striker(self) -> Player:
        """Current striker facing the next legal delivery."""
        return self.players[self.striker_index]

    def non_striker(self) -> Player:
        """Partner batter at the non-striker's end."""
        return self.players[self.non_striker_index]

    def swap_strike(self) -> None:
        """Switch striker/non-striker after odd runs or over end."""
        self.striker_index, self.non_striker_index = self.non_striker_index, self.striker_index

    def dismiss_striker(self) -> Optional[Player]:
        """Striker is out; next batter walks in on strike. Returns new striker or None if all out."""
        out = self.striker()
        self.dismissed_ids.add(out.player_id)
        non_player = self.players[self.non_striker_index]
        next_idx: Optional[int] = None
        for i, p in enumerate(self.players):
            if p.player_id in self.dismissed_ids:
                continue
            if p.player_id == non_player.player_id:
                continue
            next_idx = i
            break
        if next_idx is None:
            return None
        self.striker_index = next_idx
        return self.striker()

    def all_out(self, wickets_max: int) -> bool:
        """True when wickets lost reaches innings wicket cap."""
        return len(self.dismissed_ids) >= wickets_max


@dataclass
class InningsState:
    """Mutable innings scorecard state used by the scoring service."""

    batting_team: Team
    bowling_team: Team
    max_overs: int
    max_wickets: int
    runs: int = 0
    legal_balls: int = 0
    lineup: Optional[BattingLineup] = None

    def __post_init__(self) -> None:
        # Default batting order uses first 11 from squad.
        if self.lineup is None:
            self.lineup = BattingLineup(players=list(self.batting_team.squad[:11]))

    def overs_display(self) -> str:
        """Return overs in cricket notation, e.g. 7.3."""
        balls_in_over = self.legal_balls % 6
        completed_overs = self.legal_balls // 6
        return f"{completed_overs}.{balls_in_over}"

    def is_complete(self) -> bool:
        """Innings ends by overs exhausted or all-out."""
        completed_overs = self.legal_balls // 6
        if completed_overs >= self.max_overs:
            return True
        if self.lineup and self.lineup.all_out(self.max_wickets):
            return True
        return False

    def swap_strike(self) -> None:
        """Convenience pass-through to lineup strike swap."""
        assert self.lineup is not None
        self.lineup.swap_strike()
