from classes import *


def greeting(vm: VendingMachine) -> str:
    print("\nЧто вы хотите сделать?")
    print("1. Посмотреть доступные продукты")
    if vm.items:
        print("2. Купить продукт")
    print("3. Обслуживание")
    print("4. Выйти \n")

    choice = input("Введите номер действия: ")

    return choice


def greeting_merchant(vm: VendingMachine) -> str:
    print("\nЧто вы хотите сделать?")
    print("1. Добавить товар")

    if vm.items:
        print("2. Изъять товар")

    print("3. Внетси наличные")

    if vm.change:
        print("4. Снять наличные")

    print("5. Выйти\n")

    choice = input("Введите номер действия: ")

    return choice


def buy_item(customer: Customer,
             vm: VendingMachine):  # Функция обработки последовательности внесения средств и покупки товара

    user_bill = input('Внесите деньги, укажите номинал вносимой купюры:')
    while not user_bill.isdigit() or int(user_bill) not in vm.change.keys():
        user_bill = input('Вы внесли не деньги, внесите купюру:')

    # Внесение денег
    while user_bill != '':
        customer.credit = customer.add_cash(Money(bill=int(user_bill), amount=1))

        transaction = Transaction(trans_type=TransType.CUSTOMER_ADD_CASH, item=None,
                                  cash=Money(bill=int(user_bill), amount=1), change=None, result=True,
                                  error=ErrorType.OK_ADD_CASH)
        vm.add_transaction(transaction)

        print('... средства приняты. Баланс: ' + str(customer.credit) + '\n')
        user_bill = input('Внесите деньги, или оставьте поле пустым для перехода к выбору товара:')

    # Выбор товара, проверка ввода
    available = False
    item = None
    change = None

    while not available or item is None:
        user_item = input('Укажите номер товара:')
        item, available, change = customer.select_item(user_item)

        if item is None:
            print('Введен неверный номер товара.')

        if item is not None and not available:
            transaction = Transaction(trans_type=TransType.CUSTOMER_BUY_ITEM, item=item,
                                      cash=None, change=None, result=False,
                                      error=ErrorType.NOK_LOW_CASH)
            vm.add_transaction(transaction)

            user_bill = input('Не хватает средств для покупки товара. Внесите деньги, или выберите другой товар:')
            while user_bill != '':
                customer.credit = customer.add_cash(Money(bill=int(user_bill), amount=1))

                transaction = Transaction(trans_type=TransType.CUSTOMER_ADD_CASH, item=None,
                                          cash=Money(bill=int(user_bill), amount=1), change=None, result=True,
                                          error=ErrorType.OK_ADD_CASH)
                vm.add_transaction(transaction)

                print('... средства приняты. Баланс: ' + str(customer.credit) + '\n')
                user_bill = input('Внесите деньги, или оставьте поле пустым для перехода к выбору товара:')

    if change is None:
        print('\nСдачи нет, но вы держитесь!')

        transaction = Transaction(trans_type=TransType.CUSTOMER_GIVE_CHANGE, item=None,
                                  cash=None, change=None, result=False,
                                  error=ErrorType.NOK_NO_CHANGE)
        vm.add_transaction(transaction)

        return

    print('\n' + 'Вы выбрали ' + item.name + ', стоимость ' + str(item.price) + '. Ваш депозит - ' + str(
        customer.credit) + ', сдача - ' + str(change))

    customer.buy_item(item)

    transaction = Transaction(trans_type=TransType.CUSTOMER_BUY_ITEM, item=item,
                              cash=None, change=change, result=True,
                              error=ErrorType.OK_BUY)
    vm.add_transaction(transaction)

    if change != 0:
        vm.get_customer_change(change)


def check_bill_denomination(user_input: str, vm: VendingMachine) -> bool:
    if not user_input.isdigit():
        return False

    for bill in vm.change.keys():
        if bill // int(user_input) >= 1:
            pass
        else:
            return False
    return True


def merchant_add_item(merchant: Merchant, vm: VendingMachine):
    print('\nВведите параметры товара:')

    item_code = input('Код: ')
    while not item_code.isdigit():
        print('Указано недействительное значение. Повторите ввод')
        item_code = input('Код: ')

    item_name = input('Наименование: ')

    item_price = input('Цена: ')
    user_input_valid = check_bill_denomination(user_input=item_price, vm=vm)
    while not item_code.isdigit() or user_input_valid is False:
        print('Указано недействительное значение. Повторите ввод.')
        item_price = input('Цена: ')
        user_input_valid = check_bill_denomination(user_input=item_price, vm=vm)

    item_amount = input('Количество: ')
    while not item_amount.isdigit():
        print('Указано недействительное значение. Повторите ввод')
        item_amount = input('Количество: ')

    item = Item(code=int(item_code), name=item_name, price=int(item_price), amount=int(item_amount))

    merchant.add_item(item)

    transaction = Transaction(trans_type=TransType.MERCHANT_ADD_ITEM, item=item,
                              cash=None, change=None, result=True,
                              error=ErrorType.OK_ADD_ITEM)
    vm.add_transaction(transaction)

    merchant.show_items()


def merchant_remove_item(merchant: Merchant, vm: VendingMachine):
    merchant.show_items()
    user_input = input('\nВведите код товара, который требуется убрать:')

    while not user_input.isdigit() or int(user_input) not in vm.items.keys():
        print('Указано недействительное значение. Повторите ввод.')
        user_input = input('\nВведите код товара, который требуется убрать:')

    user_item = merchant.select_item(int(user_input))
    merchant.remove_item(user_item)

    transaction = Transaction(trans_type=TransType.MERCHANT_REMOVE_ITEM, item=user_item,
                              cash=None, change=None, result=True,
                              error=ErrorType.OK_REMOVE_ITEM)
    vm.add_transaction(transaction)

    print('Товар был успешно изъят!')


def merchant_add_change(merchant: Merchant, vm: VendingMachine):
    user_bill = input('\nУкажите номинал купюры для внесения:')
    while not user_bill.isdigit() or int(user_bill) not in vm.change.keys():
        print('Указано недействительное значение. Повторите ввод.')
        user_bill = input('\nУкажите номинал купюры для внесения:')

    user_bill_amount = input('\nУкажите количество купюр:')
    while not user_bill_amount.isdigit():
        print('Указано недействительное значение. Повторите ввод.')
        user_bill_amount = input('\nУкажите количество купюр:')

    change = {user_bill: user_bill_amount}
    merchant.add_change(Money(bill=int(user_bill), amount=int(user_bill_amount)))

    transaction = Transaction(trans_type=TransType.MERCHANT_ADD_CASH, item=None,
                              cash=None, change=change, result=True,
                              error=ErrorType.OK_ADD_CASH)
    vm.add_transaction(transaction)


def merchant_withdraw_cash(merchant: Merchant, vm: VendingMachine):
    merchant.show_change_stock()

    temp_change = {}
    for key, money in vm.change.items():
        temp_change[key] = money.amount

    transaction = Transaction(trans_type=TransType.MERCHANT_WITHDRAW, item=None,
                              cash=None, change=temp_change, result=True,
                              error=ErrorType.OK_ADD_CASH)
    vm.add_transaction(transaction)

    merchant.withdraw_cash()
    print('Деньги были успешно изъяты!')
    merchant.show_change_stock()


def main():
    vm = VendingMachine()
    merchant = Merchant(vm)
    customer = Customer(vm)

    with open("transactions.csv", mode='w', newline='', encoding='windows-1251') as file:
        writer = csv.writer(file, delimiter=';')

        writer.writerow(
            ['Дата и время', 'Номер события', 'Тип', 'Код товара', 'Имя товара', 'Цена товара', 'Количество товара',
             'Банкнота', 'Количество банкнот', 'Сдача', 'Итог операции', 'Ошибка'])

    print("Добро пожаловать в вендинговую машину!")
    while True:

        choice = greeting(vm)

        # Показать доступные товары
        if choice == '1':
            if vm.items:
                vm.show_items()
            else:
                print('В машине нет товара для покупки. Уже вызвали хозяина, он разберется.')

        # Купить товар
        elif choice == '2':
            if vm.items:
                buy_item(customer, vm)
            else:
                print('Товара нет, моожешь даже не пытаться.')

        # Обслуживание
        elif choice == '3':
            print("\nВыбран режим обслуживания:")
            choice = greeting_merchant(vm)

            # Добавить товар
            if choice == '1':
                merchant_add_item(merchant, vm)

            # Изъять товар
            elif choice == '2':
                merchant_remove_item(merchant, vm)

            # Внести наличные
            elif choice == '3':
                merchant_add_change(merchant, vm)

            # Снять наличные
            elif choice == '4':
                merchant_withdraw_cash(merchant, vm)

            # Выйти
            elif choice == '5':
                pass

        # Выйти
        elif choice == '4':
            print("Спасибо за использование вендинговой машины. До свидания!")
            break


if __name__ == "__main__":
    main()
