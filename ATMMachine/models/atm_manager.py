from typing import Dict
from ATMMachine.constants import NoteType
from ATMMachine.decorators import singleton
from ATMMachine.models.atm_machine import ATMMachine


@singleton
class ATMMachineManager:  # or ATM Repository
    def __init__(self):
        self._atms: Dict[str, ATMMachine] = dict()

    def add_atm(self, atm: ATMMachine):
        self._atms[atm.id] = atm

    def get_atm(self, atm_id: str) -> ATMMachine:
        if atm_id in self._atms:
            return self._atms[atm_id]
        else:
            print("ATM with id='{atm_id}' not found")

    def add_cash(self, atm_id: str, note_type: NoteType, count: int):
        atm = self.get_atm(atm_id)
        if atm:
            atm.add_cash(note_type, count)

    def insert_card(self, atm_id: str, card_id: str):
        atm = self.get_atm(atm_id)
        if atm:
            atm.insert_card(card_id)

    def insert_pin(self, atm_id: str, pin: str):
        atm = self.get_atm(atm_id)
        if atm:
            atm.insert_pin(pin)

    def withdraw(self, atm_id: str, amount: int):
        atm = self.get_atm(atm_id)
        if atm:
            atm.withdraw(amount)

    def remove_card(self, atm_id: str):
        atm = self.get_atm(atm_id)
        if atm:
            atm.remove_card()
