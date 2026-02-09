import threading


class AtomicInteger:
    def __init__(self, value: int = 0) -> None:
        self.value = value
        self._lock = threading.Lock()

    def getAndIncrement(self) -> int:
        with self._lock:
            ret = self.value
            self.value += 1
            return ret

    def set(self, value: int) -> None:
        with self._lock:
            self.value = value
