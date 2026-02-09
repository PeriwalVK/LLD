from abc import ABC, abstractmethod
from typing import override

from cache_system.utility_classes.concurrent_hashmap import ConcurrentHashMap


class DBStorageInterface(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get(self, key):
        pass

    @abstractmethod
    def set(self, key, value):
        pass

    @abstractmethod
    def delete(self, key):
        pass

    # def contains_key(self, key):
    #     pass


class SimpleDBStorage(DBStorageInterface):
    @override
    def __init__(self):
        self._db = ConcurrentHashMap()

    @override
    def get(self, key):
        if not self._db.contains_key(key):
            raise KeyError(f"Key {key} not found in DB")
        return self._db.get(key)

    @override
    def set(self, key, value):
        self._db.set(key, value)

    @override
    def delete(self, key):
        if not self._db.contains_key(key):
            raise KeyError(f"Key {key} not found in DB")
        self._db.delete(key)
