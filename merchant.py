from vendingmachine import VendingMachine, Item, Money


class Merchant:
    """Class representing merchant of vending machine"""

    def __init__(self, vm: VendingMachine):
        self.vm = vm

    def add_item(self, item: Item):
        """Function to add goods to vending machine"""
        self.vm.add_item(item)

    def remove_item(self, item: Item):
        """Function to remove goods to vending machine"""
        self.vm.remove_item(item)

    def add_change(self, money: Money):
        """Function to add change to vending machine"""
        self.vm.add_change(money)

    def withdraw_cash(self):
        """Function to withdraw change from vending machine"""
        self.vm.withdraw_cash()

    def show_items(self):
        """Function to show available goods of vending machine"""
        self.vm.show_items()

    def show_change_stock(self):
        """Function to show available change stock of vending machine"""
        self.vm.get_change_stock()

    def select_item(self, product_code: int) -> Item:
        """Function to select and return data of goods"""
        item = self.vm.select_item(product_code)
        return item
