class CricketScoreError(Exception):
    """Base error for the live cricket score module."""

    pass


class MatchNotLiveError(CricketScoreError):
    """Raised when score updates are attempted before/after live play."""

    pass


class InningsCompleteError(CricketScoreError):
    """Raised when a delivery is applied to a completed innings/match."""

    pass


class InvalidDeliveryError(CricketScoreError):
    """Raised when delivery input does not satisfy scoring constraints."""

    pass
