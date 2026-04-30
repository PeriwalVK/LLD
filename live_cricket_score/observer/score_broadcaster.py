from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from live_cricket_score.models.match import Match


class LiveScoreObserver(ABC):
    """Consumer interface for live score update events."""

    @abstractmethod
    def on_score_update(self, match: Match, summary: str) -> None:
        pass


class LiveScoreBroadcaster:
    """Observer subject: push-style fan-out after each scored delivery."""

    def __init__(self) -> None:
        self._observers: List[LiveScoreObserver] = []

    def attach(self, observer: LiveScoreObserver) -> None:
        """Registers an observer for future updates."""
        self._observers.append(observer)

    def detach(self, observer: LiveScoreObserver) -> None:
        """Unregisters an observer."""
        self._observers.remove(observer)

    def broadcast(self, match: Match, summary: str) -> None:
        """Notifies all observers with current match snapshot text."""
        for obs in list(self._observers):
            obs.on_score_update(match, summary)
