from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from logging_system.constants import LogLevel

try:
    from typing import override
except ImportError:  # Python < 3.12
    def override(func):
        return func

if TYPE_CHECKING:
    from logging_system.constants import LogLevel

    from logging_system.models.log_manager import LogManager
    from logging_system.observer_pattern.log_subject import LogSubject


class AbstractLogger(ABC):
    def __init__(self, level: LogLevel):
        self._level: LogLevel = level
        self._next: AbstractLogger = None

    def set_next(self, _next: AbstractLogger):
        self._next = _next

    @abstractmethod
    def display(self, message: str):
        pass

    def log(self, message: str, level: LogLevel):

        if self._level.value <= level.value:
            # if self._level.value == level.value:
            self.display(message)
        if self._next:
            self._next.log(message, level)


class InfoLogger(AbstractLogger):
    @override
    def __init__(self):
        super().__init__(LogLevel.INFO)

    def display(self, message: str) -> None:
        from logging_system.models.log_manager import LogManager

        log_subject: LogSubject = (
            LogManager.fetch_log_subject()
        )  # observer design pattern

        formatted_msg = f"[INFO]: {message}"
        log_subject.notify_observers(formatted_msg, self._level)


class ErrorLogger(AbstractLogger):
    @override
    def __init__(self):
        super().__init__(LogLevel.ERROR)

    def display(self, message: str) -> None:
        from logging_system.models.log_manager import LogManager

        log_subject: LogSubject = (
            LogManager.fetch_log_subject()
        )  # observer design pattern

        formatted_msg = f"[ERROR]: {message}"
        log_subject.notify_observers(formatted_msg, self._level)


class DebugLogger(AbstractLogger):
    @override
    def __init__(self):
        super().__init__(LogLevel.DEBUG)

    def display(self, message: str) -> None:
        from logging_system.models.log_manager import LogManager

        log_subject: LogSubject = (
            LogManager.fetch_log_subject()
        )  # observer design pattern

        formatted_msg = f"[DEBUG]: {message}"
        log_subject.notify_observers(formatted_msg, self._level)


class FatalLogger(AbstractLogger):
    @override
    def __init__(self):
        super().__init__(LogLevel.FATAL)

    def display(self, message: str) -> None:
        from logging_system.models.log_manager import LogManager

        log_subject: LogSubject = (
            LogManager.fetch_log_subject()
        )  # observer design pattern

        formatted_msg = f"[FATAL]: {message}"
        log_subject.notify_observers(formatted_msg, self._level)
