class Player:
    """Represents a player with a stable id and display name."""

    def __init__(self, player_id: str, name: str):
        self.player_id = player_id
        self.name = name

    def __repr__(self) -> str:
        return f"Player({self.player_id!r}, {self.name!r})"
