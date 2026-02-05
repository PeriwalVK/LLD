from typing import Dict
from ATMMachine.decorators import singleton
from ATMMachine.models.card import Card


@singleton
class CardManager:
    def __init__(self):
        self.cards: Dict[str, Card] = dict()

    def __str__(self):
        return f"CardManager(mem_address={id(self)}, cards={[card.__str__() for card in self.cards.values()]})"

    def add_card(self, card: Card):
        self.cards[card.id] = card

    def authenticate_pin(self, card_id: str, pin: str) -> bool:
        return self.cards[card_id].auth(pin)

    def fetch_balance(self, card_id: str) -> float:
        return self.cards[card_id].account.balance

    def is_valid_card(self, card_id: str) -> bool:
        return card_id in self.cards
