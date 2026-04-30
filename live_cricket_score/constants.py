from enum import Enum, auto


class MatchStatus(Enum):
    """Lifecycle of a cricket match in this simplified model."""

    SCHEDULED = auto()
    LIVE = auto()
    COMPLETED = auto()


class DeliveryKind(Enum):
    """Type of delivery from a scoring perspective."""

    LEGAL = auto()
    WIDE = auto()
    NO_BALL = auto()

class WicketKind(Enum):
    """Enumerates wicket outcomes that can be attached to a delivery."""

    BOWLED = auto()
    CAUGHT = auto()
    RUN_OUT = auto()
    LBW = auto()
    STUMP = auto()
    HIT_WICKET = auto()
    OBSTRUCTING_FIELD = auto()
    RETIRED_OUT = auto()
    TIME_OUT = auto()
    OTHER = auto()
