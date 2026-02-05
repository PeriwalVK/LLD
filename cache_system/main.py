from __future__ import annotations

import sys
import os


""" Get the absolute path of the folder containing main.py """
root_folder = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)  # path/to/project_root

""" Add that folder to the list of places Python looks for modules """
if root_folder not in sys.path:
    sys.path.insert(0, root_folder)
    # adds root_folder to start of sys.path list, so it gets prioritised while looking at imports


if __name__ == "__main__":
    from cache_system.models.cache import Cache
    from cache_system.strategy.cache_storage import ICacheStorage, InMemoryCacheStorage
    from cache_system.strategy.db_storage import DBStorageInterface, SimpleDBStorage
    from cache_system.strategy.eviction_policy import IEvictionPolicy, LRUEvictionPolicy
    from cache_system.strategy.write_policy import IWritePolicy, WriteThroughPolicy

    # from cache_system.models.cache import Cache
    try:
        # // Set a small capacity for the in-memory cache (e.g., 5 items)
        cacheStorage: ICacheStorage = InMemoryCacheStorage(5)
        # // The underlying persistent store (DB storage) can be assumed to have large or unlimited capacity.
        dbStorage: DBStorageInterface = SimpleDBStorage()
        # // Create the write-through policy (writes concurrently to both storages).
        writePolicy: IWritePolicy = WriteThroughPolicy()
        # // Create the LRU eviction algorithm.
        evictionAlg: IEvictionPolicy = LRUEvictionPolicy()
        # // Create the cache with 4 executor threads to guarantee per-key ordering.
        cache: Cache = Cache(cacheStorage, dbStorage, writePolicy, evictionAlg, 4)

        # // Demonstrate write operations.
        cache.set("A", "Apple")
        cache.set("B", "Banana")
        cache.set("C", "Cherry")
        cache.set("D", "Durian")
        cache.set("E", "Elderberry")

        # // At this point, the in-memory cache is at capacity.
        # // The next write will trigger eviction (of the least recently used key) from the cache.
        cache.set("F", "Fig")

        # overwriting/updating existing keys
        cache.set("D", "Date")

        # // Demonstrate read operations.
        try:
            valueA = cache.get("A")
            print(f"A: {valueA}")
        except Exception as e:
            print(f"A is evicted or not found in cache. ERROR FOUND IS: {e}")

        try:
            valueX = cache.get("X")
            print(f"X: {valueX}")
        except Exception as e:
            print(f"X is evicted or not found in cache. ERROR FOUND IS: {e}")

        valueF = cache.get("F")
        print(f"F: {valueF}")

        # // Update an existing key and then read it to demonstrate read-your-own-writes.
        cache.set("B", "Blueberry")
        valueB = cache.get("B")
        print(f"B: {valueB}")

        # // Shut down executors when finished.

        print(f"D: {cache.get('D')}")
        cache.shutdown()

    except Exception as e:
        print(f"An error occurred: {e}")
