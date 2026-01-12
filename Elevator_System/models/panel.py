from abc import ABC

from Elevator_System.models.button import Button


class OuterPanel():
    def __init__(self):
        self.is_active = True
        self.up: Button = Button()
        self.down: Button = Button()
    
    def press_up(self):
        if self.is_active:
            self.up.press()
    
    def press_down(self):
        if self.is_active:
            self.down.press()
    
    def turn_off(self):
        self.is_active = False
