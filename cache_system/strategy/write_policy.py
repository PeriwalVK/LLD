from abc import ABC, abstractmethod
from concurrent.futures import Future, ThreadPoolExecutor
import threading
from typing import List, override

from cache_system.strategy.cache_storage import ICacheStorage
from cache_system.strategy.db_storage import DBStorageInterface


class IWritePolicy(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def write(
        self,
        key,
        value,
        cache_storage: ICacheStorage = None,
        db_storage: DBStorageInterface = None,
    ):
        pass


class WriteThroughPolicy(IWritePolicy):

    @override
    def __init__(self):
        pass

    @override
    def write(
        self,
        key,
        value,
        cache_storage: ICacheStorage = None,
        db_storage: DBStorageInterface = None,
    ):
        workers = 2
        if cache_storage is None:
            workers -= 1
        if db_storage is None:
            workers -= 1
            # raise ValueError("Cache storage and DB storage cannot be None")
        if workers == 0:
            raise ValueError(
                "Cache storage and DB storage - both cannot be None simultenously"
            )
        prefix = f"[{threading.current_thread().name}-key={key}]"
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures: List[Future] = []
            if cache_storage:
                futures.append(executor.submit(cache_storage.set, key, value))
                print(f"{prefix}: writing key={key} and val={value} to cache storage")
            if db_storage:
                futures.append(executor.submit(db_storage.set, key, value))
                print(f"{prefix}: writing key={key} and val={value} to DB storage")

            for future in futures:
                future.result()
