from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from live_cricket_score.constants import MatchStatus
from live_cricket_score.models.innings import InningsState
from live_cricket_score.models.team import Team


@dataclass
class Match:
    """Match aggregate root containing two innings and transition state."""

    match_id: str
    venue: str
    team_home: Team
    team_away: Team
    max_overs_per_innings: int
    max_wickets: int = 10
    status: MatchStatus = MatchStatus.SCHEDULED
    innings_list: List[InningsState] = field(default_factory=list)
    current_innings_index: int = 0

    def start(self, bat_first: Team, bowl_first: Team) -> None:
        """Initializes both innings and marks the match as LIVE."""
        if self.status != MatchStatus.SCHEDULED:
            raise ValueError("Match already started")
        first = InningsState(
            batting_team=bat_first,
            bowling_team=bowl_first,
            max_overs=self.max_overs_per_innings,
            max_wickets=self.max_wickets,
        )
        # second_bat = team_opponent(bat_first, self.team_home, self.team_away)
        # second_bowl = team_opponent(bowl_first, self.team_home, self.team_away)
        second = InningsState(
            # batting_team=second_bat,
            # bowling_team=second_bowl,
            batting_team=bowl_first,
            bowling_team=bat_first,
            max_overs=self.max_overs_per_innings,
            max_wickets=self.max_wickets,
        )
        self.innings_list = [first, second]
        self.status = MatchStatus.LIVE
        self.current_innings_index = 0

    def current_innings(self) -> InningsState:
        """Returns the innings currently accepting deliveries."""
        return self.innings_list[self.current_innings_index]

    def advance_innings_if_needed(self) -> None:
        """Moves from first to second innings, then marks completion."""
        if not self.innings_list:
            return
        cur = self.current_innings()
        if cur.is_complete() and self.current_innings_index == 0:
            self.current_innings_index = 1
        if self.current_innings_index == 1 and self.current_innings().is_complete():
            self.status = MatchStatus.COMPLETED


# def team_opponent(team: Team, home: Team, away: Team) -> Team:
#     """Returns the other team from this match."""
#     if team.team_id == home.team_id:
#         return away
#     if team.team_id == away.team_id:
#         return home
#     raise ValueError("Team is not part of this match")
