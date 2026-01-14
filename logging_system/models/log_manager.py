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
    @staticmethod
    def build_logger_chain() -> AbstractLogger:
        info_logger: AbstractLogger = InfoLogger()
        error_logger: AbstractLogger = ErrorLogger()
        debug_logger: AbstractLogger = DebugLogger()
        fatal_logger: AbstractLogger = FatalLogger()

        info_logger.set_next(error_logger)
        error_logger.set_next(debug_logger)
        debug_logger.set_next(fatal_logger)

        return info_logger

    @staticmethod
    def build_log_subject():
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
