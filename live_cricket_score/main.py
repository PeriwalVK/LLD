from __future__ import annotations

import os
import sys

# Ensure package-style imports work when this file is executed directly.
root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_folder not in sys.path:
    sys.path.insert(0, root_folder)

from live_cricket_score.constants import DeliveryKind, MatchStatus
from live_cricket_score.models.ball_delivery import BallDelivery
from live_cricket_score.models.match import Match
from live_cricket_score.models.player import Player
from live_cricket_score.models.team import Team
from live_cricket_score.observer.score_broadcaster import LiveScoreBroadcaster, LiveScoreObserver
from live_cricket_score.services.live_score_service import LiveScoreService


class ConsoleFeedObserver(LiveScoreObserver):
    """Simple observer that prints updates to the terminal."""

    def __init__(self, label: str) -> None:
        self._label = label

    def on_score_update(self, match: Match, summary: str) -> None:
        print(f"[{self._label}] {summary} | match={match.status.name}")


def _xi(prefix: str) -> list[Player]:
    """Builds a sample playing XI for demos."""
    return [Player(f"{prefix}-{i}", f"{prefix} Player {i}") for i in range(1, 12)]


if __name__ == "__main__":
    # Teams and match setup.
    india = Team("IND", "India", _xi("IND"))
    aus = Team("AUS", "Australia", _xi("AUS"))

    match = Match(
        match_id="M-2025-001",
        venue="MCG",
        team_home=aus,
        team_away=india,
        max_overs_per_innings=2,
        max_wickets=10,
    )
    match.start(bat_first=india, bowl_first=aus)

    # Broadcast to one or more UI channels.
    broadcaster = LiveScoreBroadcaster()
    broadcaster.attach(ConsoleFeedObserver("Web"))
    # broadcaster.attach(ConsoleFeedObserver("Mobile"))

    svc = LiveScoreService(match, broadcaster)

    # Sample ball-by-ball feed covering legal balls, extras, and a wicket.
    sequence = [
        BallDelivery(DeliveryKind.LEGAL, runs_off_bat=1),
        BallDelivery(DeliveryKind.LEGAL, runs_off_bat=4),
        BallDelivery(DeliveryKind.WIDE, extra_runs=0),
        BallDelivery(DeliveryKind.LEGAL, runs_off_bat=0),
        BallDelivery(DeliveryKind.LEGAL, runs_off_bat=6),
        BallDelivery(DeliveryKind.LEGAL, runs_off_bat=1),
        BallDelivery(DeliveryKind.LEGAL, is_wicket=True),
        BallDelivery(DeliveryKind.NO_BALL, runs_off_bat=2, extra_runs=0),
        BallDelivery(DeliveryKind.LEGAL, runs_off_bat=2),
        BallDelivery(DeliveryKind.LEGAL, runs_off_bat=1),
        BallDelivery(DeliveryKind.LEGAL, runs_off_bat=1),
        BallDelivery(DeliveryKind.LEGAL, runs_off_bat=0),
        BallDelivery(DeliveryKind.LEGAL, runs_off_bat=0),
        BallDelivery(DeliveryKind.LEGAL, runs_off_bat=0),
    ]

    for ball in sequence:
        svc.deliver_ball(ball)

    # Demo sanity checks: first innings should be done and match should be in second innings.
    assert match.status == MatchStatus.LIVE
    assert match.current_innings_index == 1
