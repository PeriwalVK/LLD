class UserValueDto:
    def __init__(self, user_id: str, value: float):
        self.user_id: str = user_id
        self.value: float = value