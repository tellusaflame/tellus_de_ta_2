from datetime import datetime
import csv


class Item:
    def __init__(self, code: int, name: str, price: int, amount: int):
        self.code = code
        self.name = name
        self.price = price
        self.amount = amount


class Money:
    def __init__(self, bill: int, amount: int):
        self.bill = bill
        self.amount = amount


class TransType:
    CUSTOMER_ADD_CASH = 'Внесение наличных покупателем'
    CUSTOMER_BUY_ITEM = 'Покупка товара покупателем'
    CUSTOMER_GIVE_CHANGE = 'Выдача сдачи покупателю'
    MERCHANT_ADD_CASH = 'Внесение наличных торговцем'
    MERCHANT_ADD_ITEM = 'Внесение товара торговцем'
    MERCHANT_REMOVE_ITEM = 'Изъятие товара торговцем'
    MERCHANT_WITHDRAW = 'Изъятие наличных торговцем'


class ErrorType:
    NOK_LOW_CASH = 'Недостаточно средств'
    OK_BUY = 'Покупка товара выполнена'
    NOK_NO_CHANGE = 'Нет сдачи'
    OK_ADD_CASH = 'Наличные внесены'
    OK_ADD_ITEM = 'Товар добавлен'
    OK_REMOVE_ITEM = 'Товар изъят'
    OK_WITHDRAW = 'Деньги сняты'


class Transaction:
    def __init__(self, trans_type: str, item: Item, cash: Money, change: dict, result: bool,
                 error: str):
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.trans_type = trans_type
        self.item = item
        self.cash = cash
        self.change = change
        self.result = result
        self.error = error


class VendingMachine:
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
        self.transactions[self.transaction_counter] = transaction
        self.transaction_counter += 1

        with open("transactions.csv", mode='a', newline='', encoding='utf8') as file:
            writer = csv.writer(file, delimiter=';')

            writer.writerow(
                [transaction.timestamp,
                 self.transaction_counter,
                 transaction.trans_type,
                 transaction.item.code if transaction.item else '',
                 transaction.item.name if transaction.item else '',
                 transaction.item.price if transaction.item else '',
                 transaction.item.amount if transaction.item else '',
                 transaction.cash.bill if transaction.cash else '',
                 transaction.cash.amount if transaction.cash else '',
                 transaction.change if transaction.change else '',
                 transaction.result,
                 transaction.error])

    def show_items(self):
        for key, item in self.items.items():
            print(str(item.code) + ' | ' + item.name + ' | ' + str(item.price))

    def add_item(self, item: Item):
        new_item = item
        self.items[item.code] = new_item

    def remove_item(self, item: Item):
        self.items.pop(item.code)

    def buy_item(self, item: Item):
        self.items[item.code].amount -= 1
        if self.items[item.code].amount == 0:
            self.items.pop(item.code)

    def get_balance(self) -> int:  # Посчитать баланс
        summ = 0
        for key, value in self.change.items():
            summ += self.change[key].bill * self.change[key].amount
        return summ

    def get_change_stock(self):  # Вывести содержимое размена
        for key, value in self.change.items():
            print(str(key) + ': ' + str(self.change[key].amount))

    def get_customer_change(self, customer_change: dict):  # Изъять сдачу из размена (выдать сдачу)
        for bill, amount in customer_change.items():
            self.change[bill].amount -= amount

    def add_cash(self, money: Money):  # Внесение средств покупателя
        self.change[money.bill].amount += money.amount
        self.credit += money.bill * money.amount

        return self.credit

    def add_change(self, money: Money):  # Пополнение размена
        self.change[money.bill].amount += money.amount
        self.get_change_stock()

    def withdraw_cash(self):  # , bill: int):  # Снять деньги
        # self.change[bill].amount = 0
        for key, value in self.change.items():
            self.change[key].amount = 0

    def check_empty(self):
        if self.items:
            return 1

    def select_item(self, product_code: int):
        if product_code in self.items.keys():
            return self.items[product_code]
        else:
            return None

    def calc_customer_change(self, credit: int, cost: int):
        customer_change = {}
        actual_change = 0
        total_change = credit - cost

        if total_change == 0:
            return 0

        for key, money in self.change.items():
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


class Customer:
    def __init__(self, vm: VendingMachine):
        self.vm = vm
        self.credit = 0

    def add_cash(self, money: Money):
        self.credit = self.vm.add_cash(money)
        return self.credit

    def select_item(self, product_code):
        item = None
        available = False
        change = None

        if not product_code.isdigit():
            return item, available, change

        item = self.vm.select_item(int(product_code))
        if item is None:
            return item, available, change

        if self.credit - item.price >= 0:
            available = True
        else:
            available = False
        change = self.vm.calc_customer_change(credit=self.credit, cost=item.price)

        return item, available, change

    def buy_item(self, item: Item):
        self.vm.buy_item(item)
        self.vm.credit = 0
        self.credit = 0

    def get_customer_change(self, customer_change: dict):
        self.vm.get_customer_change(customer_change)


class Merchant:
    def __init__(self, vm: VendingMachine):
        self.vm = vm

    def add_item(self, item: Item):
        self.vm.add_item(item)

    def remove_item(self, item: Item):
        self.vm.remove_item(item)

    def add_change(self, money: Money):
        self.vm.add_change(money)

    def withdraw_cash(self):
        self.vm.withdraw_cash()

    def show_items(self):
        self.vm.show_items()

    def show_change_stock(self):
        self.vm.get_change_stock()

    def select_item(self, product_code: int) -> Item:
        item = self.vm.select_item(product_code)
        return item
