from __future__ import annotations

from live_cricket_score.constants import DeliveryKind, MatchStatus
from live_cricket_score.exceptions import InningsCompleteError, MatchNotLiveError
from live_cricket_score.models.ball_delivery import BallDelivery
from live_cricket_score.models.innings import InningsState
from live_cricket_score.models.match import Match
from live_cricket_score.observer.score_broadcaster import LiveScoreBroadcaster


class LiveScoreService:
    """
    Application service: validates match state, applies scoring rules, notifies subscribers.
    """

    def __init__(self, match: Match, broadcaster: LiveScoreBroadcaster):
        self._match = match
        self._broadcaster = broadcaster

    @property
    def match(self) -> Match:
        return self._match

    def deliver_ball(self, ball: BallDelivery) -> None:
        """
        Applies one delivery to current innings and emits observer updates.
        Also advances innings/match when terminal conditions are met.
        """
        if self._match.status != MatchStatus.LIVE:
            raise MatchNotLiveError("Match is not live")

        innings = self._match.current_innings()
        if innings.is_complete():
            self._match.advance_innings_if_needed()
            if self._match.status == MatchStatus.COMPLETED:
                raise InningsCompleteError("Match finished")
            innings = self._match.current_innings()
            if innings.is_complete():
                raise InningsCompleteError("Innings already complete")

        self._apply_delivery(innings, ball)
        self._match.advance_innings_if_needed()
        self._broadcaster.broadcast(self._match, self._build_summary(innings))

    def _apply_delivery(self, innings: InningsState, ball: BallDelivery) -> None:
        """Encodes simplified scoring rules for legal/wide/no-ball events."""
        lineup = innings.lineup
        assert lineup is not None

        if ball.kind == DeliveryKind.WIDE:
            # Wide adds one base run plus any additional extras; no legal ball consumed.
            innings.runs += 1 + ball.extra_runs
            return

        if ball.kind == DeliveryKind.NO_BALL:
            # No-ball adds one base run and can include bat runs/extras; no legal ball consumed.
            innings.runs += 1 + ball.runs_off_bat + ball.extra_runs
            return

        # Legal delivery
        innings.runs += ball.runs_off_bat
        if ball.is_wicket:
            lineup.dismiss_striker()
        elif ball.runs_off_bat % 2 == 1:
            # Odd runs rotate strike.
            innings.swap_strike()

        innings.legal_balls += 1
        if innings.legal_balls % 6 == 0 and not innings.is_complete():
            # End of over rotates strike in this model.
            innings.swap_strike()

    def _build_summary(self, last_innings: InningsState) -> str:
        """Builds a compact scoreline for observers/UI logs."""
        lineup = last_innings.lineup
        assert lineup is not None
        base = (
            f"{last_innings.batting_team.name} {last_innings.runs}/"
            f"{len(lineup.dismissed_ids)} ({last_innings.overs_display()} ov)"
        )
        if last_innings.is_complete():
            return f"{base} - innings complete"
        striker = lineup.striker()
        non = lineup.non_striker()
        return f"{base} - {striker.name}*, {non.name}"
