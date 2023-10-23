import csv
import os
from typing import Union
from dotenv import load_dotenv
from modules.vendingmachine.item import Item
from modules.vendingmachine.money import Money
from modules.transactions.transactions import Transaction
from modules.transactions.transtype import TransType
from modules.transactions.errortype import ErrorType

load_dotenv()


class VendingMachine:
    """Class representing a vending machine and its structure"""

    def __init__(self):
        self.items = {
            1: Item(code=1, name="Марс", price=10, amount=10),
            2: Item(code=2, name="Сникерс", price=20, amount=5),
            3: Item(code=3, name="Баунти", price=500, amount=1),
        }

        self.change = {
            5000: Money(bill=5000, amount=0),
            2000: Money(bill=2000, amount=0),
            1000: Money(bill=1000, amount=0),
            500: Money(bill=500, amount=0),
            200: Money(bill=200, amount=0),
            100: Money(bill=100, amount=0),
            50: Money(bill=50, amount=0),
            10: Money(bill=10, amount=3),
        }

        self.balance = self.get_balance()

        self.customer_credit = 0

        self.transactions = {}
        self.transaction_counter = 0

        self.merchant_secret = os.getenv("MERCHANT_CODE")

    def vm_greeting(self):
        print("Здравствуйте! Ниже список товаров, доступных к покупке: ")

    def check_customer_merchant(self):
        user_input = input(
            "\n"
            "Пожалуйста, укажите номер желаемого продукта, или введите 0 чтобы выйти:"
        )
        # if user_input == self.merchant_secret:
        return user_input == self.merchant_secret, user_input

    def show_items(self):
        """Function to print all the available goods"""
        print("\n" "# | Название | Цена | Доступно" "\n" "----------------------------")
        for item in self.items.values():
            item_string = f"{item.code} | {item.name} | {item.price} | {item.amount}"
            print(item_string)

    def check_customer_balance_enough(self, item_price) -> bool:
        return item_price <= self.customer_credit

    def add_cash(self, money: Money):
        """Function to account customer money"""
        self.change[money.bill].amount += money.amount
        self.customer_credit += money.bill * money.amount

        print(f"Ваш баланс равен {self.customer_credit}")

        transaction = Transaction(
            trans_type=TransType.CUSTOMER_ADD_CASH,
            item=None,
            cash=Money(bill=money.bill, amount=1),
            change=None,
            result=True,
            error=ErrorType.OK_ADD_CASH,
        )
        self.add_transaction(transaction)

    def calc_customer_change(self, total_change: int) -> Union[dict, None]:
        """Function to calculate and control customer change"""
        customer_change = {}
        actual_change = 0

        for money in self.change.values():
            temp_amount = money.amount
            if total_change >= money.bill and money.amount > 0:
                customer_change[money.bill] = 0
                while total_change >= money.bill and temp_amount > 0:
                    customer_change[money.bill] += 1
                    total_change -= money.bill
                    temp_amount -= 1
                    actual_change += money.bill

        if not customer_change or actual_change < total_change:
            return None

        return customer_change

    def get_customer_change(self, customer_change: dict):
        """Function to process customer change"""
        for bill, amount in customer_change.items():
            self.change[bill].amount -= amount

    def buy_item(self, item: Item):
        """Function to perform an account of position to buy"""
        self.items[item.code].amount -= 1
        if self.items[item.code].amount == 0:
            self.items.pop(item.code)
        self.customer_credit -= item.price

        transaction = Transaction(
            trans_type=TransType.CUSTOMER_BUY_ITEM,
            item=item,
            cash=None,
            change=None,
            result=True,
            error=ErrorType.OK_BUY,
        )
        self.add_transaction(transaction)

    def set_transactions_file(self):
        with open(
            "transactions.csv", mode="w", newline="", encoding="windows-1251"
        ) as file:
            writer = csv.writer(file, delimiter=";")

            writer.writerow(
                [
                    "Дата и время",
                    "Номер события",
                    "Тип",
                    "Код товара",
                    "Имя товара",
                    "Цена товара",
                    "Количество товара",
                    "Банкнота",
                    "Количество банкнот",
                    "Сдача",
                    "Итог операции",
                    "Ошибка",
                ]
            )

    def add_transaction(self, transaction):
        """Function to track all important vending machine transactions"""

        self.transactions[self.transaction_counter] = transaction
        self.transaction_counter += 1

        with open(
            "transactions.csv", mode="a", newline="", encoding="windows-1251"
        ) as file:
            writer = csv.writer(file, delimiter=";")

            writer.writerow(
                [
                    transaction.timestamp,
                    self.transaction_counter,
                    transaction.trans_type,
                    transaction.item.code if transaction.item else "",
                    transaction.item.name if transaction.item else "",
                    transaction.item.price if transaction.item else "",
                    transaction.item.amount if transaction.item else "",
                    transaction.cash.bill if transaction.cash else "",
                    transaction.cash.amount if transaction.cash else "",
                    transaction.change if transaction.change else "",
                    transaction.result,
                    transaction.error,
                ]
            )

    def check_if_merchant(self, user_input: int, secret_code: int) -> bool:
        return user_input == int(secret_code)

    def greeting_merchant(self):
        print("\nДобро пожаловать в режим обслуживания!")

    def check_bill_denomination(self, user_input: str) -> bool:
        """Function to check if item price is correct"""
        if not user_input.isdigit():
            return False

        for money in self.change.values():
            result = int(user_input) % money.bill == 0
        return result

    def add_item(self, item: Item):
        """Function to add new (or replace existing) goods position"""
        new_item = item
        self.items[item.code] = new_item

        self.show_items()

        transaction = Transaction(
            trans_type=TransType.MERCHANT_ADD_ITEM,
            item=item,
            cash=None,
            change=None,
            result=True,
            error=ErrorType.OK_ADD_ITEM,
        )
        self.add_transaction(transaction)

    def remove_item(self, item: Item):
        """Function to remove an existing goods position"""
        self.items.pop(item.code)
        print(f"Товар #{item.code} - {item.name} был успешно изъят!")

        transaction = Transaction(
            trans_type=TransType.MERCHANT_REMOVE_ITEM,
            item=item,
            cash=None,
            change=None,
            result=True,
            error=ErrorType.OK_REMOVE_ITEM,
        )
        self.add_transaction(transaction)

    def get_balance(self) -> int:
        """Function to calculate an actual balance of vending machine"""
        calc_balance = 0
        for value in self.change.values():
            calc_balance += value.bill * value.amount
        return calc_balance

    def get_change_stock(self):
        """Function to print an actual change stock of vending machine"""
        print("\n" "Остаток средств:" "\n" "Купюра: количество")
        for money in self.change.values():
            print(f"{money.bill}: {money.amount}")

    def add_change(self, money: Money):
        """Function to account merchant adding money to vending machine"""
        self.change[money.bill].amount += money.amount

        print(f"Купюры были внесены: номинал {money.bill}, количество {money.amount}")

        transaction = Transaction(
            trans_type=TransType.MERCHANT_ADD_CASH,
            item=None,
            cash=None,
            change={money.bill, money.amount},
            result=True,
            error=ErrorType.OK_ADD_CASH,
        )
        self.add_transaction(transaction)

    def withdraw_cash(self):
        """Function to perform cash withdraw by merchant"""
        temp_change = {}
        for money in self.change.values():
            temp_change[money.bill] = money.amount

        transaction = Transaction(
            trans_type=TransType.MERCHANT_WITHDRAW,
            item=None,
            cash=None,
            change=temp_change,
            result=True,
            error=ErrorType.OK_WITHDRAW,
        )
        self.add_transaction(transaction)

        for money in self.change.values():
            money.amount = 0

        print("\n" "Деньги были полностью изъяты из машины!")

    def select_item(self, product_code: int):
        """Function to return data of selected goods"""
        if product_code in self.items:
            return self.items[product_code]
        return None

    def check_items_available(self) -> bool:
        return self.items.keys() is not None


#
#         transaction = Transaction(
#             trans_type=TransType.CUSTOMER_ADD_CASH,
#             item=None,
#             cash=Money(bill=int(user_bill), amount=1),
#             change=None,
#             result=True,
#             error=ErrorType.OK_ADD_CASH,
#         )
#         vm.add_transaction(transaction)

#
#         if item is not None and not available:
#             transaction = Transaction(
#                 trans_type=TransType.CUSTOMER_BUY_ITEM,
#                 item=item,
#                 cash=None,
#                 change=None,
#                 result=False,
#                 error=ErrorType.NOK_LOW_CASH,
#             )
#             vm.add_transaction(transaction)

#
#                 transaction = Transaction(
#                     trans_type=TransType.CUSTOMER_ADD_CASH,
#                     item=None,
#                     cash=Money(bill=int(user_bill), amount=1),
#                     change=None,
#                     result=True,
#                     error=ErrorType.OK_ADD_CASH,
#                 )
#                 vm.add_transaction(transaction)
#
#
#         transaction = Transaction(
#             trans_type=TransType.CUSTOMER_GIVE_CHANGE,
#             item=None,
#             cash=None,
#             change=None,
#             result=False,
#             error=ErrorType.NOK_NO_CHANGE,
#         )
#         vm.add_transaction(transaction)
#
#
#
#     transaction = Transaction(
#         trans_type=TransType.CUSTOMER_BUY_ITEM,
#         item=item,
#         cash=None,
#         change=change,
#         result=True,
#         error=ErrorType.OK_BUY,
#     )
#     vm.add_transaction(transaction)
#
#
#     transaction = Transaction(
#         trans_type=TransType.MERCHANT_ADD_ITEM,
#         item=item,
#         cash=None,
#         change=None,
#         result=True,
#         error=ErrorType.OK_ADD_ITEM,
#     )
#     vm.add_transaction(transaction)
#
#
#     transaction = Transaction(
#         trans_type=TransType.MERCHANT_REMOVE_ITEM,
#         item=user_item,
#         cash=None,
#         change=None,
#         result=True,
#         error=ErrorType.OK_REMOVE_ITEM,
#     )
#     vm.add_transaction(transaction)
#

#
#     transaction = Transaction(
#         trans_type=TransType.MERCHANT_ADD_CASH,
#         item=None,
#         cash=None,
#         change=change,
#         result=True,
#         error=ErrorType.OK_ADD_CASH,
#     )
#     vm.add_transaction(transaction)
#

#
#     transaction = Transaction(
#         trans_type=TransType.MERCHANT_WITHDRAW,
#         item=None,
#         cash=None,
#         change=temp_change,
#         result=True,
#         error=ErrorType.OK_ADD_CASH,
#     )
#     vm.add_transaction(transaction)
