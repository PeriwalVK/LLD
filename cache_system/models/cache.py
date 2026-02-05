import threading
from cache_system.utility_classes.key_based_executor import KeyBasedThreadExecutor
from cache_system.strategy.cache_storage import ICacheStorage
from cache_system.strategy.db_storage import DBStorageInterface
from cache_system.strategy.eviction_policy import IEvictionPolicy
from cache_system.strategy.write_policy import IWritePolicy


class Cache:
    def __init__(
        self,
        cache_storage: ICacheStorage,
        db_storage: DBStorageInterface,
        write_policy: IWritePolicy,
        eviction_policy: IEvictionPolicy,
        num_threads: int,
    ):
        self._cache_storage: ICacheStorage = cache_storage
        self._db_storage: DBStorageInterface = db_storage
        self._write_policy: IWritePolicy = write_policy
        self._eviction_policy: IEvictionPolicy = eviction_policy

        self.num_threads: int = num_threads
        self.executor = KeyBasedThreadExecutor(num_threads=num_threads)

    def _get_task(self, key):
        prefix = f"[{threading.current_thread().name}-key={key}]"
        try:
            if not self._cache_storage.contains_key(key):
                print(f"""{prefix}: Cache miss.""")
                if self._db_storage:
                    print(f"""{prefix}: fetching from DB""")
                    val = self._db_storage.get(key)
                    print(f"""{prefix}: fetched {key}={val} from DB""")

                    # self._write_policy.write(
                    #     key, val, cache_storage=self._cache_storage
                    # )

                    self._set_task(key, val, on_db=False)
                    # raise KeyError(f"Key {key} not found in DB")
                else:
                    raise KeyError(f"{prefix}: Key {key} not found in DB")
            else:
                print(f"""{prefix}: Cache hit.""")
                self._eviction_policy.mark_key_accessed(key)
            
            return self._cache_storage.get(key)
        except KeyError as e:
            raise e

    def _set_task(self, key, value, on_db=True):
        prefix = f"[{threading.current_thread().name}-key={key}]"

        if self._cache_storage.contains_key(key):
            print(f"""{prefix}: key: {key} already found in cache""")
            self._write_policy.write(
                key,
                value,
                cache_storage=self._cache_storage,
                db_storage=self._db_storage if on_db else None,
            )
            self._eviction_policy.mark_key_accessed(key)
        else:
            # new key
            print(f"{prefix}: key {key} is a new entry for cache")
            while (
                self._cache_storage.size() >= self._cache_storage.get_capacity()
            ):  # keep evicting
                print(
                    f"""{prefix}: Cache full. current size: {self._cache_storage.size()}; capacity: {self._cache_storage.get_capacity()}"""
                )
                evicted_key = self._eviction_policy.evict()
                print(f"""{prefix}: evicted key: {evicted_key}""")

                # to avoid deadlock, check if eviction and current key has same executor index,
                # if yes, then do it here only, else assign to corresponding thread.

                evicted_key_executor_index = self.executor.get_executor_index(
                    evicted_key
                )
                current_key_executor_index = self.executor.get_executor_index(key)

                if evicted_key_executor_index == current_key_executor_index:
                    self._cache_storage.delete(evicted_key)
                else:
                    removal_future = self.executor.submit(
                        evicted_key,
                        self._cache_storage.delete,
                        evicted_key,
                    )
                    removal_future.result()

            self._write_policy.write(
                key,
                value,
                cache_storage=self._cache_storage,
                db_storage=self._db_storage if on_db else None,
            )
            self._eviction_policy.mark_key_accessed(key)

    def get(self, key):
        # def task():
        print(f"********************************* get(key={key})****************************************")
        future = self.executor.submit(key, self._get_task, key)
        return future.result()

    def set(self, key, value, on_db=True):
        print(f"********************** set(key={key}, value={value}, on_db={on_db})******************")
        future = self.executor.submit(key, self._set_task, key, value, on_db)
        print()
        return future.result()

    def shutdown(self, wait=True, **kwargs):
        self.executor.shutdown(wait=wait, **kwargs)
