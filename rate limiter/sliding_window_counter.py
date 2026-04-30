import time

# TODO: Fix
class SlidingWindowCounterRateLimiter:
    """
    Sliding Window Counter Rate Limiter.

    Combines counts from the previous window and the current window
    to approximate a true sliding window.
    """

    def __init__(self, limit: int, window_size: int):
        """
        limit       : maximum requests allowed in the window
        window_size : window duration in seconds
        """

        # Maximum requests allowed
        self.limit = limit

        # Window duration
        self.window_size = window_size

        # Count of requests in the current window
        self.current_count = 0

        # Count of requests in the previous window
        self.previous_count = 0

        # Start time of the current window
        self.window_start = int(time.time())

    def allow_request(self) -> bool:

        now = int(time.time())
        elapsed = now - self.window_start

        # If window has completely moved
        if elapsed >= self.window_size:

            # Shift windows
            self.previous_count = self.current_count
            self.current_count = 0

            # Start new window
            self.window_start = now
            elapsed = 0

        # Weight of the previous window
        weight = (self.window_size - elapsed) / self.window_size

        # Estimated number of requests in sliding window
        estimated = self.previous_count * weight + self.current_count

        # If limit reached, reject request
        if estimated >= self.limit:
            return False

        # Accept request
        self.current_count += 1
        return True