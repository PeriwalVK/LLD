from dataclasses import dataclass
from typing import Optional

from live_cricket_score.constants import DeliveryKind, WicketKind


@dataclass(frozen=True)
class BallDelivery:
    """
    Immutable description of one scored event.

    runs_off_bat: 0-6.
    extra_runs: additional extras beyond base wide/no-ball run handled in service.
    wicket_kind: optional classification when is_wicket=True.
    """

    kind: DeliveryKind
    runs_off_bat: int = 0
    is_wicket: bool = False
    extra_runs: int = 0
    wicket_kind: Optional[WicketKind] = None

    def __post_init__(self) -> None:
        # Basic numeric guards.
        if self.runs_off_bat < 0 or self.runs_off_bat > 6:
            raise ValueError("runs_off_bat must be 0..6")
        if self.extra_runs < 0:
            raise ValueError("extra_runs cannot be negative")

        # Simplified dismissal constraints by delivery type.
        if self.is_wicket:
            if self.kind == DeliveryKind.NO_BALL:
                if self.wicket_kind != WicketKind.RUN_OUT:
                    raise ValueError("On a no-ball, only run outs are allowed as wicket kind")
            elif self.kind == DeliveryKind.WIDE:
                if self.wicket_kind not in (WicketKind.RUN_OUT, WicketKind.STUMP):
                    raise ValueError("On a wide, only run outs and stumpings are allowed as wicket kind")
            elif self.kind != DeliveryKind.LEGAL:
                raise ValueError(
                    "Wickets can only be recorded on legal deliveries, run outs on no-balls, or run outs/stumpings on wides"
                )
