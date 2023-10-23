from typing import Union
from modules.vendingmachine.vendingmachine import VendingMachine
from modules.vendingmachine.item import Item
from modules.vendingmachine.money import Money


class Customer:
    """Class representing customer of vending machine"""

    def __init__(self, vm: VendingMachine):
        self.vm = vm
        self.credit = 0

    def select_item(self, selected_number: str) -> Union[Item, None]:
        """Function to perform selection of desired goods of vending machine"""
        item = None

        # selected_number = input("Please select desired product with its code number, or type 0 to exit:")
        while not item:
            if selected_number.isdigit() and int(selected_number) == 0:
                return None

            if (
                not selected_number.isdigit()
                or int(selected_number) not in self.vm.items.keys()
            ):
                selected_number = input(
                    "Некорректный ввод. Пожалуйста, укажите номер желаемого продукта, или введите 0 чтобы выйти:"
                )

            elif int(selected_number) in self.vm.items.keys():
                item = self.vm.select_item(int(selected_number))
                return item

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
