from __future__ import annotations
from abc import ABC, abstractmethod
from typing import override

from logging_system.constants import LogLevel
from logging_system.observer_pattern.log_subject import LogSubject


class AbstractLogger(ABC):
    def __init__(self, level: LogLevel):
        self._level: LogLevel = level
        self._next: AbstractLogger = None

    def set_next(self, _next: AbstractLogger):
        self._next = _next

    @abstractmethod
    def display(self, message: str, log_subject: LogSubject):
        pass
    
    def log(self, message: str, level: LogLevel, log_subject: LogSubject):
        if self._level.value <= level.value:
        # if self._level.value == level.value:
            self.display(message,log_subject)
        if self._next:
            self._next.log(message, level, log_subject)


class InfoLogger(AbstractLogger):
    @override
    def __init__(self):
        super().__init__(LogLevel.INFO)

    def display(self, message: str, log_subject: LogSubject) -> None:
        formatted_msg = f"[INFO]: {message}"
        log_subject.notify_observers(formatted_msg, self._level)


class ErrorLogger(AbstractLogger):
    @override
    def __init__(self):
        super().__init__(LogLevel.ERROR)

    def display(self, message: str, log_subject: LogSubject) -> None:
        formatted_msg = f"[ERROR]: {message}"
        log_subject.notify_observers(formatted_msg, self._level)


class DebugLogger(AbstractLogger):
    @override
    def __init__(self):
        super().__init__(LogLevel.DEBUG)

    def display(self, message: str, log_subject: LogSubject) -> None:
        formatted_msg = f"[DEBUG]: {message}"
        log_subject.notify_observers(formatted_msg, self._level)

class FatalLogger(AbstractLogger):
    @override
    def __init__(self):
        super().__init__(LogLevel.FATAL)

    def display(self, message: str, log_subject: LogSubject) -> None:
        formatted_msg = f"[FATAL]: {message}"
        log_subject.notify_observers(formatted_msg, self._level)