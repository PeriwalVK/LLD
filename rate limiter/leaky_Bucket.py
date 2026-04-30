import time
from collections import deque


class LeakyBucketRateLimiter:
    """
    Leaky Bucket Rate Limiter.

    Requests enter the bucket.
    The bucket leaks at a constant rate.
    If the bucket is full, new requests are rejected.
    """

    def __init__(self, capacity: int, leak_rate: float):
        """
        capacity: maximum number of requests that can wait in the bucket
        leak_rate: requests processed per second
        """
        self.capacity = capacity
        self.leak_rate = leak_rate

        # queue storing timestamps of accepted requests
        self.queue = deque()

        # last time leakage was processed
        self.last_check = time.time()

    def allow_request(self) -> bool:
        now = int(time.time())

        # Calculate how many requests should leak
        elapsed = now - self.last_check
        leaked = int(elapsed * self.leak_rate)

        # Remove leaked requests
        for _ in range(min(leaked, len(self.queue))):
            self.queue.popleft()

        # # Update last check time
        # if leaked > 0:
        #     self.last_check = now
        self.last_check = now

        if leaked > 0:
            print(f"leaked : {leaked}")
        print(f"curr queue size : {len(self.queue)}")

        # If bucket full → reject
        if len(self.queue) >= self.capacity:
            return False

        # Accept request
        self.queue.append(now)
        return True

limiter = LeakyBucketRateLimiter(capacity=7, leak_rate=5)

for i in range(20):
    if i==10:
        time.sleep(1) 
    print(f"i={i}, allow_request={limiter.allow_request()}")