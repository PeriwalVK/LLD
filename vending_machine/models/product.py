class Product:
    _id = 0

    def __init__(self, name: str, price: float):
        self.id: str = str(Product._id); Product._id += 1
        self.name: str = name
        self.price: float = price
