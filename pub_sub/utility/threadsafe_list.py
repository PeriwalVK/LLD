import threading
from typing import List

class ThreadSafeList[T]:
    def __init__(self):
        self._lst: List[T] = []
        self._lock = threading.Lock()

    def append(self, x: T):
        with self._lock:
            self._lst.append(x)

    def remove(self, x: T):
        with self._lock:
            self._lst.remove(x)

    def snapshot(self) -> List[T]:
        # safe way to iterate without holding the lock
        with self._lock:
            return list(self._lst)