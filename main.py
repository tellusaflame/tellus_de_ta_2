from modules.vendingmachine.vendingmachine import VendingMachine
from modules.vendingmachine.customer import Customer
from modules.vendingmachine.merchant import Merchant
from modules.vendingmachine.money import Money


def main():
    """Main function to control all the interactions and vending machine entities"""
    vm = VendingMachine()
    vm.set_transactions_file()

    merchant = Merchant(vm)
    customer = Customer(vm)

    vm.vm_greeting()

    while True:
        vm.show_items()

        is_merchant, user_input = vm.check_customer_merchant()

        if is_merchant:
            vm.greeting_merchant()
            while True:
                choice = merchant.select_options()

                if choice == "1":
                    merchant.add_item()

                elif choice == "2":
                    merchant.remove_item()

                elif choice == "3":
                    merchant.add_change()

                elif choice == "4":
                    merchant.withdraw_cash()

                elif choice == "5":
                    vm.get_change_stock()

                elif choice == "6":
                    break
            continue

        customer_item = customer.select_item(user_input)

        if customer_item is None:
            if vm.customer_credit > 0:
                change = vm.calc_customer_change(vm.customer_credit)
                if change is None:
                    print(
                        "Извините, в машине недостаточно сдачи. Пожалуйста, свяжитесь с владельцем машины, "
                        "или позвоните 112."
                    )
                    break
                print(f"Спасибо за покупки! Вот ваша сдача: {change}")
                vm.get_customer_change(change)
            else:
                print("Всего хорошего. До свидания!")
            break

        print(f"Вы выбрали {customer_item.name}, цена = {customer_item.price}")

        while vm.check_customer_balance_enough(customer_item.price) is False:
            try:
                money = int(
                    input(
                        f"Пожалуйста, вставьте купюры чтобы пополнить баланс до {customer_item.price - vm.customer_credit}: "
                    )
                )
                if money not in vm.change:
                    continue
                customer.add_cash(Money(bill=money, amount=1))
            except ValueError:
                continue

        vm.buy_item(customer_item)
        print(
            f"Вы приобрели {customer_item.name}! " f"Ваш баланс: {vm.customer_credit}"
        )


if __name__ == "__main__":
    main()
