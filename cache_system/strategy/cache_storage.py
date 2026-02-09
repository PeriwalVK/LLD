from abc import ABC, abstractmethod
from typing import override

from cache_system.utility_classes.concurrent_hashmap import ConcurrentHashMap


class ICacheStorage(ABC):
    @abstractmethod
    def __init__(self, capacity: int):
        self._capacity: int = capacity

    @abstractmethod
    def get(self, key):
        pass

    @abstractmethod
    def set(self, key, value):
        pass

    @abstractmethod
    def delete(self, key):
        pass

    @abstractmethod
    def contains_key(self, key) -> bool:
        pass

    @abstractmethod
    def size(self):
        pass

    def get_capacity(self):
        return self._capacity


class InMemoryCacheStorage(ICacheStorage):
    @override
    def __init__(self, capacity: int):
        # self._capacity: int = capacity

        super().__init__(capacity)
        self._cache: ConcurrentHashMap = ConcurrentHashMap()

    @override
    def get(self, key):
        return self._cache.get(key)

    @override
    def set(self, key, value):
        self._cache.set(key, value)

    @override
    def delete(self, key):
        self._cache.delete(key)

    @override
    def contains_key(self, key) -> bool:
        return self._cache.contains_key(key)

    @override
    def size(self):
        return self._cache.size()
