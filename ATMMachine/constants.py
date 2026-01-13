from enum import Enum


class NoteType(Enum):
    NOTE_2000 = 2000
    NOTE_500 = 500
    NOTE_200 = 200
    NOTE_100 = 100

class ATMStateType(Enum):
    IDLE = "IDLE"
    CARD_INSERTED = "CARD_INSERTED"
    PIN_AUTHENTICATED = "PIN_AUTHENTICATED"


    
