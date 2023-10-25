class Item:
    """Class representing some form of goods"""

    def __init__(self, code: int, name: str, price: int, amount: int):
        self.code = code
        self.name = name
        self.price = price
        self.amount = amount
