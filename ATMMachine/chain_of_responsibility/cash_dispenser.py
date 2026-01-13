from __future__ import annotations
from typing import TYPE_CHECKING

from ATMMachine.constants import NoteType

if TYPE_CHECKING:
    from ATMMachine.models.atm_machine import ATMMachine


class CashDispenser:
    def __init__(self, note_type: NoteType):
        self.note_type: NoteType = note_type
        self._soft_count = 0
        # self.atm_machine = atm_machine
        self.next: CashDispenser = None

    def set_next(self, cash_dispenser: CashDispenser):
        self.next = cash_dispenser

    def dispense(self, atm_machine: ATMMachine, amount: int):
        if self._soft_count:
            atm_machine.remove_cash(self.note_type, self._soft_count)
            print(
                f"Dispensing {self._soft_count} x {self.note_type.value} notes = {self._soft_count * self.note_type.value}"
            )
        if self.next:
            self.next.dispense(
                atm_machine, amount - self._soft_count * self.note_type.value
            )

    def can_dispense(self, atm_machine: ATMMachine, amount: int) -> bool:
        _max_notes = min(
            atm_machine.cash.get(self.note_type, 0), amount // self.note_type.value
        )
        for note_cnt in range(_max_notes, -1, -1):
            remaining_amt = amount - note_cnt * self.note_type.value
            # if remaining_amt:
            #     if self.next:
            #         if self.next.can_dispense(atm_machine, remaining_amt):
            #             self._soft_count = note_cnt
            #             return True
            #     else:
            #         return False
            # else:
            #     self._soft_count = note_cnt
            #     return True
            if (not remaining_amt) or (
                self.next and self.next.can_dispense(atm_machine, remaining_amt)
            ):
                self._soft_count = note_cnt
                return True
        return False


class CashDispenserManager:
    @staticmethod
    def build_cash_handler_chain() -> CashDispenser:
        _2000_handler: CashDispenser = CashDispenser(NoteType.NOTE_2000)
        _500_handler: CashDispenser = CashDispenser(NoteType.NOTE_500)
        _200_handler: CashDispenser = CashDispenser(NoteType.NOTE_200)
        _100_handler: CashDispenser = CashDispenser(NoteType.NOTE_100)

        _2000_handler.set_next(_500_handler)
        _500_handler.set_next(_200_handler)
        _200_handler.set_next(_100_handler)

        return _2000_handler
