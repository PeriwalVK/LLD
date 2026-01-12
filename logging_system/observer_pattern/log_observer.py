from abc import ABC, abstractmethod
from typing import override


class LogObserver(ABC):
    @abstractmethod
    def update(self, msg: str):
        pass


class ConsoleLogger(LogObserver):
    @override
    def update(self, msg: str):
        print(f"[ConsoleLogger]: writing to console: '{msg}'")


class FileLogger(LogObserver):
    @override
    def update(self, msg: str):
        print(f"[FileLogger]: writing to file: '{msg}'")


class PrometheusLogger(LogObserver):
    @override
    def update(self, msg: str):
        print(f"[PrometheusLogger]: pushing to prometheus: '{msg}'")


class EmailAlert(LogObserver):
    @override
    def update(self, msg: str):
        print(f"[EmailAlert]: sending email: '{msg}'")


class KibanaLogger(LogObserver):
    @override
    def update(self, msg: str):
        print(f"[KibanaLogger]: pushing to kibana: '{msg}'")
