from typing import Optional
from modules.vendingmachine.vendingmachine import VendingMachine
from modules.vendingmachine.item import Item
from modules.vendingmachine.money import Money


class Customer:
    """Class representing customer of vending machine"""

    def __init__(self, vm: VendingMachine):
        self.vm = vm
        self.credit = 0

    def select_item(self, selected_number: int) -> Optional[Item]:
        """Function to perform selection of desired goods of vending machine"""
        while True:
            if selected_number == 0:
                return None
            if selected_number not in self.vm.items.keys():
                try:
                    selected_number = int(
                        input(
                            "Некорректный ввод. Пожалуйста, укажите номер желаемого продукта, или введите 0 чтобы выйти:"
                        )
                    )
                except ValueError:
                    continue
            else:
                return self.vm.select_item(selected_number)

    def add_cash(self, money: Money):
        """Function to account customer adding cash to vending machine"""
        self.credit = self.vm.add_cash(money)

    def buy_item(self, item: Item):
        """Function to perform buy action"""
        self.vm.buy_item(item)
        self.vm.credit = 0
        self.credit = 0

    def get_customer_change(self, customer_change: dict):
        """Function to perform change calculation"""
        self.vm.get_customer_change(customer_change)
