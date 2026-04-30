import time


class FixedWindowRateLimiter:
    """
    Fixed Window Counter Rate Limiter.

    Requests are counted within a fixed time window.
    Once the window expires, the counter resets.
    """

    def __init__(self, limit: int, window_size: int):
        """
        limit       : maximum requests allowed in a window
        window_size : window duration in seconds
        """

        # Maximum allowed requests per window
        self.limit = limit

        # Window size in seconds
        self.window_size = window_size

        # Current window identifier
        self.current_window = int(time.time()) // window_size

        # Number of requests in the current window
        self.counter = 0

    def allow_request(self) -> bool:

        now = int(time.time())

        # Determine which window the current request belongs to
        window = now // self.window_size

        # If we moved to a new window, reset the counter
        if window != self.current_window:
            self.current_window = window
            self.counter = 0

        # If limit already reached, reject request
        if self.counter >= self.limit:
            return False

        # Otherwise accept request
        self.counter += 1
        return True
    


limiter = FixedWindowRateLimiter(limit=7, window_size=1)

for i in range(20):
    if i==10:
        time.sleep(1) 
    print(f"i={i}, allow_request={limiter.allow_request()}")