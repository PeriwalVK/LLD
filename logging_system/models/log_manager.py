from __future__ import annotations
from typing import TYPE_CHECKING

# if TYPE_CHECKING:
from logging_system.chain_of_responsibility.abstract_logger import (
    AbstractLogger,
    DebugLogger,
    ErrorLogger,
    FatalLogger,
    InfoLogger,
)
from logging_system.constants import LogLevel
from logging_system.observer_pattern.log_observer import (
    ConsoleLogger,
    EmailAlert,
    FileLogger,
    KibanaLogger,
    LogObserver,
    PrometheusLogger,
)
from logging_system.observer_pattern.log_subject import LogSubject


class LogManager:
    _log_subject = None
    _logger_chain = None

    @staticmethod
    def _build_logger_chain() -> AbstractLogger:
        info_logger: AbstractLogger = InfoLogger()
        error_logger: AbstractLogger = ErrorLogger()
        debug_logger: AbstractLogger = DebugLogger()
        fatal_logger: AbstractLogger = FatalLogger()

        info_logger.set_next(error_logger)
        error_logger.set_next(debug_logger)
        debug_logger.set_next(fatal_logger)

        return info_logger

    @staticmethod
    def _build_log_subject():
        subject: LogSubject = LogSubject()

        console_logger: LogObserver = ConsoleLogger()
        file_logger: LogObserver = FileLogger()
        prometheus_logger: LogObserver = PrometheusLogger()
        email_alert: LogObserver = EmailAlert()
        kibana_logger: LogObserver = KibanaLogger()

        subject.attach(LogLevel.INFO, file_logger)
        subject.attach(LogLevel.INFO, console_logger)

        subject.attach(LogLevel.ERROR, prometheus_logger)

        subject.attach(LogLevel.DEBUG, kibana_logger)

        subject.attach(LogLevel.FATAL, email_alert)

        return subject

    @staticmethod
    def fetch_log_subject() -> LogSubject:
        if not LogManager._log_subject:
            LogManager._log_subject = LogManager._build_log_subject()
        return LogManager._log_subject

    @staticmethod
    def fetch_logger_chain() -> AbstractLogger:
        if not LogManager._logger_chain:
            LogManager._logger_chain = LogManager._build_logger_chain()
        return LogManager._logger_chain
