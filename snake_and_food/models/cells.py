from snake_and_food.constants import Symbol


class Cell:
    def __init__(self, row:int, col: int, symbol: Symbol = Symbol.EMPTY):
        self.row = row
        self.col = col
        self.symbol = symbol

    def set_symbol(self, symbol: Symbol):
        self.symbol = symbol
    
    def get_symbol(self) -> Symbol:
        return self.symbol

    def __str__(self) -> str:
        return self.symbol.value
