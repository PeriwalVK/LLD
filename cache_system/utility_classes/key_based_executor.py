from concurrent.futures import Executor, Future, ThreadPoolExecutor
from typing import List


class KeyBasedThreadExecutor(Executor):
    """
    Routes tasks to one of N single-threaded executors based on a key.

    Guarantees:
    - Tasks with the same key execute sequentially
    - Tasks with different keys may execute in parallel
    """

    def __init__(self, num_threads: int):
        self.num_threads = num_threads
        self.executors: List[ThreadPoolExecutor] = [
            ThreadPoolExecutor(max_workers=1, thread_name_prefix=f"Executor-{i}")
            for i in range(num_threads)
        ]
        # print(f"  -> Created {num_threads} underlying executors.")

        # # Use built-in hash() to support strings, ints, etc.
        # # abs() is needed because hash() can be negative
        self.hash = lambda key: abs(hash(key))
        # self.hash = lambda key: key

    def get_executor_index(self, key):
        return self.hash(key) % self.num_threads

    # We modify the signature to accept a 'key', so it knows where to route the task.
    def submit(self, key, fn, /, *args, **kwargs) -> Future:
        """
        Submit a task associated with a key.
        Tasks with the same key are executed sequentially.
        """
        idx = self.get_executor_index(key)
        return self.executors[idx].submit(fn, *args, **kwargs)

    def __enter__(self):
        # print("  -> Entering context manager...")
        return self

    # Implement shutdown separately so it can be called manually if not using context manager.
    def shutdown(self, wait=True, **kwargs):
        # print("  -> Shutting down all inner executors...")
        for executor in self.executors:
            executor.shutdown(wait=wait, **kwargs)
        # print("  -> All inner executors successfully shut down.")

    def __exit__(self, exc_type, exc_value, traceback):
        self.shutdown(wait=True)
        # print("  -> Exiting context manager...")
        # return False to ensure all tasks finish, but do not suppress exceptions
        return False
