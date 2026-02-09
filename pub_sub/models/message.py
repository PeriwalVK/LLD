class Message[T]:
    def __init__(self, message: T):
        self.message: T = message

    def get_message(self) -> T:
        return self.message

    def __repr__(self):
        return f"""Message("{self.message}")"""
