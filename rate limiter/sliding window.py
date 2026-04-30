import time
import datetime as dt


class SlidingWindowRateLimiter:
    """
    Sliding window rate limiter using per-second buckets and
    window-boundary based cleanup.
    """

    def __init__(self, limit: int, window_size: int):
        # Maximum requests allowed in the sliding window
        self.limit = limit

        # Window duration in seconds
        self.window_size = window_size

        # Circular array storing request counts per second
        self.buckets = [0] * window_size

        # Total requests currently in the window
        self.total = 0

        # Last time we processed a request
        self.last_seen_time = 0

    def allow_request(self) -> bool:
        # now = int(time.time())
        now = int(dt.datetime.now().timestamp())

        # # First request initialization
        # if self.last_seen_time is None:
        #     self.last_seen_time = now

        # Compute window boundaries
        last_window_start = self.last_seen_time - self.window_size + 1
        current_window_start = now - self.window_size + 1

        # If the gap is larger than the window,
        # the entire previous window is irrelevant
        if self.last_seen_time < current_window_start:
            self.buckets = [0] * self.window_size
            self.total = 0

        else:
            # Reset buckets that moved outside the window
            # t = last_window_start
            for t in range(last_window_start, current_window_start):
            # while t < current_window_start:
                idx = t % self.window_size
                self.total -= self.buckets[idx]
                self.buckets[idx] = 0
                # t += 1

        # Update last seen time
        self.last_seen_time = now   

        # Enforce rate limit
        if self.total >= self.limit:
            return False

        # Record the request
        idx = now % self.window_size
        self.buckets[idx] += 1
        self.total += 1

        return True