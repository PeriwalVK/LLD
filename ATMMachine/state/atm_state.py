from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, override

from ATMMachine.chain_of_responsibility.cash_dispenser import CashDispenserManager
from ATMMachine.constants import ATMStateType
from ATMMachine.models.card_manager import CardManager

if TYPE_CHECKING:
    from ATMMachine.models.atm_machine import ATMMachine


class ATMState(ABC):
    @abstractmethod
    def __init__(self, atm_state_type: ATMStateType):
        self.state_type: ATMStateType = atm_state_type
        self.card_manager: CardManager = CardManager()

    def insert_card(self, card_id: str):
        print(f"CAN'T INSERT CARD IN {self.state_type.value} STATE")
        return self

    def insert_pin(self, pin: str):
        print(f"CAN'T INSERT PIN IN {self.state_type.value} STATE")
        return self

    def withdraw(self, amount: int):
        print(f"CAN'T WITHDRAW CASH IN {self.state_type.value} STATE")
        return self

    def remove_card(self):
        print(f"CAN'T REMOVE CARD IN {self.state_type.value} STATE")
        return self


class IDLEState(ATMState):
    @override
    def __init__(self, atm_machine: ATMMachine):
        super().__init__(ATMStateType.IDLE)
        self.atm_machine: ATMMachine = atm_machine

    @override
    def insert_card(self, card_id: str):
        if self.atm_machine._set_current_card(card_id):
            print("Card successfully inserted.")
            return self.atm_machine._card_inserted_state
        else:
            print(f"Couldn't insert Card {card_id}.")
            return self


class CardInsertedState(ATMState):
    @override
    def __init__(self, atm_machine: ATMMachine):
        super().__init__(ATMStateType.CARD_INSERTED)
        self.atm_machine: ATMMachine = atm_machine

    @override
    def insert_pin(self, pin: str):
        if self.card_manager.authenticate_pin(self.atm_machine._current_card_id, pin):
            print("PIN successfully authenticated.")
            return self.atm_machine._pin_authenticated_state
        else:
            print("Invalid PIN. Try again...")
            return self

    @override
    def remove_card(self):
        self.atm_machine._unset_current_card()
        print("CARD successfully removed.")
        return self.atm_machine._idle_state


class PinAuthenticatedState(ATMState):
    @override
    def __init__(self, atm_machine: ATMMachine):
        super().__init__(ATMStateType.PIN_AUTHENTICATED)
        self.atm_machine: ATMMachine = atm_machine

    @override
    def withdraw(self, amount: int):
        if self.atm_machine.balance < amount:
            print(
                f"CANT WITHDRAW {amount} as INSUFFICIENT FUNDS IN MACHINE - currently {self.atm_machine.balance}."
            )
            return self
        elif self.card_manager.fetch_balance(self.atm_machine._current_card_id) < amount:
            print(
                f"CANT WITHDRAW {amount} as current balance is just {self.card_manager.fetch_balance(self.atm_machine._current_card_id)}."
            )
            return self
        else:
            cash_dispenser = CashDispenserManager.build_cash_handler_chain()
            if cash_dispenser.can_dispense(self.atm_machine, amount):
                cash_dispenser.dispense(self.atm_machine, amount)
                print("Withdrawal successful.")
                return self.atm_machine._idle_state
            else:
                print("Can not dispense requested amount fully...try different amount")
                return self

    @override
    def remove_card(self):
        self.atm_machine._unset_current_card()
        print("CARD successfully removed.")
        return self.atm_machine._idle_state
