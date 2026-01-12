from typing import Dict, List
from logging_system.constants import LogLevel
from logging_system.observer_pattern.log_observer import LogObserver


class LogSubject:
    def __init__(self):
        self._observers: Dict[LogLevel, List[LogObserver]] = {
            # LogLevel.INFO: [],
            # LogLevel.ERROR: [],
            # LogLevel.DEBUG: [],
        }

    def attach(self, level: LogLevel, observer: LogObserver):
        obs_list = self._observers.get(level, [])
        obs_list.append(observer)
        self._observers[level] = obs_list

    def notify_observers(self, message: str, level: LogLevel):
        for observer in self._observers.get(level, []):
            observer.update(message)

    # def detach(self, observer: LogObserver):
    #     self._observers.remove(observer)
