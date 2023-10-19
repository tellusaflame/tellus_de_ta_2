import csv


class Item:
    """Class representing some form of goods"""

    def __init__(self, code: int, name: str, price: int, amount: int):
        self.code = code
        self.name = name
        self.price = price
        self.amount = amount


class Money:
    """Class representing some form of money"""

    def __init__(self, bill: int, amount: int):
        self.bill = bill
        self.amount = amount


class VendingMachine:
    """Class representing a vending machine and its structure"""

    def __init__(self):
        self.items = {
            1: Item(code=1, name="Mars", price=10, amount=10),
            2: Item(code=2, name="Snikers", price=20, amount=5),
            3: Item(code=3, name="Bounty", price=500, amount=1),
        }

        self.change = {
            5000: Money(bill=5000, amount=1),
            2000: Money(bill=2000, amount=2),
            1000: Money(bill=1000, amount=3),
            500: Money(bill=500, amount=10),
            200: Money(bill=200, amount=10),
            100: Money(bill=100, amount=10),
            50: Money(bill=50, amount=10),
            10: Money(bill=10, amount=10),
        }

        self.balance = self.get_balance()

        self.credit = 0

        self.transactions = {}
        self.transaction_counter = 0

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

    def show_items(self):
        """Function to print all the available goods"""
        for item in self.items.values():
            print(str(item.code) + " | " + item.name + " | " + str(item.price))

    def add_item(self, item: Item):
        """Function to add new (or replace existing) goods position"""
        new_item = item
        self.items[item.code] = new_item

    def remove_item(self, item: Item):
        """Function to remove an existing goods position"""
        self.items.pop(item.code)

    def buy_item(self, item: Item):
        """Function to perform an account of position to buy"""
        self.items[item.code].amount -= 1
        if self.items[item.code].amount == 0:
            self.items.pop(item.code)

    def get_balance(self) -> int:
        """Function to calculate an actual balance of vending machine"""
        summ = 0
        for value in self.change.values():
            summ += value.bill * value.amount
        return summ

    def get_change_stock(self):
        """Function to print an actual change stock of vending machine"""
        for money in self.change.values():
            print(str(money.bill) + ": " + str(money.amount))

    def get_customer_change(self, customer_change: dict):
        """Function to process customer change"""
        for bill, amount in customer_change.items():
            self.change[bill].amount -= amount

    def add_cash(self, money: Money):
        """Function to account customer money"""
        self.change[money.bill].amount += money.amount
        self.credit += money.bill * money.amount

        return self.credit

    def add_change(self, money: Money):
        """Function to account merchant adding money to vending machine"""
        self.change[money.bill].amount += money.amount
        self.get_change_stock()

    def withdraw_cash(self):
        """Function to perform cash withdraw by merchant"""
        for money in self.change.values():
            money.amount = 0

    def select_item(self, product_code: int):
        """Function to return data of selected goods"""
        if product_code in self.items:
            return self.items[product_code]
        return None

    def calc_customer_change(self, credit: int, cost: int):
        """Function to calculate and control customer change"""
        customer_change = {}
        actual_change = 0
        total_change = credit - cost

        if total_change == 0:
            return 0

        for money in self.change.values():
            temp_amount = money.amount
            if total_change >= money.bill and money.amount > 0:
                customer_change[money.bill] = 0
                while total_change >= money.bill and temp_amount > 0:
                    customer_change[money.bill] += 1
                    total_change -= money.bill
                    temp_amount -= 1
                    actual_change += money.bill

        if not customer_change or actual_change < (credit - cost):
            return None

        return customer_change
