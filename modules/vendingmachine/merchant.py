from modules.vendingmachine.vendingmachine import VendingMachine
from modules.vendingmachine.item import Item
from modules.vendingmachine.money import Money


class Merchant:
    """Class representing merchant of vending machine"""

    def __init__(self, vm: VendingMachine):
        self.vm = vm

    def select_options(self) -> str:
        """Function to display merchant actions and process user input"""
        print("\nЧто вы хотите сделать?")
        print("1. Добавить товар")

        if self.vm.items:
            print("2. Изъять товар")

        print("3. Внетси наличные")

        if self.vm.change:
            print("4. Снять наличные")

        print("5. Показать остаток наличных")

        print("6. Выйти\n")

        choice = input("Введите номер действия: ")

        return choice

    def add_item(self):
        """Function to add goods to vending machine"""
        while True:
            print("\nВведите параметры товара:")
            try:
                item_code = int(input("Код: "))
                if item_code <= 0:
                    raise ValueError

                item_name = input("Наименование: ")

                item_price = int(input("Цена: "))
                if item_price <= 0:
                    raise ValueError

                user_input_valid = self.vm.check_bill_denomination(
                    user_input=item_price
                )
                if not user_input_valid:
                    raise ValueError

                item_amount = int(input("Количество: "))
                if item_amount <= 0:
                    raise ValueError

                break

            except ValueError:
                print("Указано недействительное значение. Повторите ввод")
                continue

        item = Item(
            code=item_code,
            name=item_name,
            price=item_price,
            amount=item_amount,
        )

        self.vm.add_item(item)

    def remove_item(self):
        """Function to remove goods to vending machine"""
        self.vm.show_items()
        user_input = input("\nВведите код товара, который требуется убрать:")

        while not user_input.isdigit() or int(user_input) not in self.vm.items.keys():
            print("Указано недействительное значение. Повторите ввод.")
            user_input = input("\nВведите код товара, который требуется убрать:")

        item = self.vm.select_item(int(user_input))
        self.vm.remove_item(item)
        self.vm.show_items()

    def add_change(self):
        """Function to add change to vending machine"""
        user_bill = input("\nУкажите номинал купюры для внесения:")
        while not user_bill.isdigit() or int(user_bill) not in self.vm.change.keys():
            print("Указано недействительное значение. Повторите ввод.")
            user_bill = input("\nУкажите номинал купюры для внесения:")

        user_bill_amount = input("\nУкажите количество купюр:")
        while not user_bill_amount.isdigit():
            print("Указано недействительное значение. Повторите ввод.")
            user_bill_amount = input("\nУкажите количество купюр:")

        self.vm.add_change(Money(bill=int(user_bill), amount=int(user_bill_amount)))
        self.vm.get_change_stock()

    def withdraw_cash(self):
        """Function to withdraw change from vending machine"""
        self.vm.get_change_stock()
        self.vm.withdraw_cash()
        self.vm.get_change_stock()
