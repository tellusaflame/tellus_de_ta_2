from datetime import datetime
from modules.vendingmachine.item import Item
from modules.vendingmachine.money import Money


class Transaction:
    """Class holding all the information about vending machine important transactions"""

    def __init__(
        self,
        trans_type: str,
        item: Item,
        cash: Money,
        change: dict,
        result: bool,
        error: str,
    ):
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.trans_type = trans_type
        self.item = item
        self.cash = cash
        self.change = change
        self.result = result
        self.error = error
