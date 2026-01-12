from abc import ABC


class Button(ABC):
    def __init__(self):
        self._pressed: bool = False

    def press(self):
        if not self._pressed:
            self._pressed = True
            # impl logic
        else:
            print("Already pressed...")
    
    def release(self):
        if self._pressed:
            self._pressed = False
        else:
            print("Button is not pressed...")
    
    def is_pressed(self):
        return self._pressed
    
