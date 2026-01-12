from logging_system.chain_of_responsibility.abstract_logger import AbstractLogger
from logging_system.constants import LogLevel
from logging_system.models.log_manager import LogManager
from logging_system.observer_pattern.log_subject import LogSubject


class Logger:
    def __init__(self):
        self._logger_chain: AbstractLogger = (
            LogManager.build_logger_chain()
        )  # chain of responsibility
        self._log_subject: LogSubject = (
            LogManager.build_log_subject()
        )  # observer design pattern

    def info(self, message: str) -> None:
        self._log(message, LogLevel.INFO)

    def error(self, message: str) -> None:
        self._log(message, LogLevel.ERROR)

    def debug(self, message: str) -> None:
        self._log(message, LogLevel.DEBUG)

    def fatal(self, message: str) -> None:
        self._log(message, LogLevel.FATAL)

    def _log(self, message: str, level: LogLevel):
        self._logger_chain.log(message, level, self._log_subject)
