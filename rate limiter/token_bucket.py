import time


class TokenBucketRateLimiter:
    """
    Token Bucket Rate Limiter.

    Tokens are added to the bucket at a constant rate.
    Each request consumes one token.
    If no tokens are available, the request is rejected.
    """

    def __init__(self, capacity: int, refill_rate: float):
        """
        capacity: maximum number of tokens the bucket can hold
        refill_rate: tokens added per second
        """
        self.capacity = capacity
        self.refill_rate = refill_rate

        # current number of tokens
        self.tokens = capacity

        # last time tokens were refilled
        self.last_refill_time = time.time()

    def allow_request(self) -> bool:
        now = time.time()

        # Calculate how much time has passed
        elapsed = now - self.last_refill_time

        # Add new tokens based on elapsed time
        refill = elapsed * self.refill_rate

        self.tokens = min(self.capacity, self.tokens + refill)

        # Update last refill time
        self.last_refill_time = now

        # If no tokens left → reject
        if self.tokens < 1:
            return False

        # Consume one token
        self.tokens -= 1
        return True


limiter = TokenBucketRateLimiter(capacity=7, refill_rate=5)

for i in range(20):
    if i==10:
        time.sleep(1) 
    print(f"i={i}, allow_request={limiter.allow_request()}")




