from vendingmachine import VendingMachine, Item, Money


class Customer:
    """Class representing customer of vending machine"""
    def __init__(self, vm: VendingMachine):
        self.vm = vm
        self.credit = 0

    def add_cash(self, money: Money):
        """Function to account customer adding cash to vending machine"""
        self.credit = self.vm.add_cash(money)
        return self.credit

    def select_item(self, product_code):
        """Function to perform selection of desired goods of vending machine"""
        item = None
        available = False
        change = None

        if not product_code.isdigit():
            return item, available, change

        item = self.vm.select_item(int(product_code))
        if item is None:
            return item, available, change

        available = self.credit - item.price >= 0
        change = self.vm.calc_customer_change(credit=self.credit, cost=item.price)

        return item, available, change

    def buy_item(self, item: Item):
        """Function to perform buy action"""
        self.vm.buy_item(item)
        self.vm.credit = 0
        self.credit = 0

    def get_customer_change(self, customer_change: dict):
        """Function to perform change calculation"""
        self.vm.get_customer_change(customer_change)
