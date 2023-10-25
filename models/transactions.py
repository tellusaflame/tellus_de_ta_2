from enum import Enum
from datetime import datetime
from models.item import Item
from models.money import Money


class TransType(Enum):
    """Class with list of transaction type prompts"""

    CUSTOMER_ADD_CASH = "Внесение наличных покупателем"
    CUSTOMER_BUY_ITEM = "Покупка товара покупателем"
    CUSTOMER_GIVE_CHANGE = "Выдача сдачи покупателю"
    MERCHANT_ADD_CASH = "Внесение наличных торговцем"
    MERCHANT_ADD_ITEM = "Внесение товара торговцем"
    MERCHANT_REMOVE_ITEM = "Изъятие товара торговцем"
    MERCHANT_WITHDRAW = "Изъятие наличных торговцем"


class ErrorType(Enum):
    """Class with list of transaction error type prompts"""

    NOK_LOW_CASH = "Недостаточно средств"
    OK_BUY = "Покупка товара выполнена"
    NOK_NO_CHANGE = "Нет сдачи"
    OK_ADD_CASH = "Наличные внесены"
    OK_ADD_ITEM = "Товар добавлен"
    OK_REMOVE_ITEM = "Товар изъят"
    OK_WITHDRAW = "Деньги сняты"
    OK_CUSTOMER_CHANGE = "Сдача выдана"


class Transaction:
    """Class holding all the information about vending machine important transactions"""

    def __init__(
            self,
            trans_type: str,
            result: bool,
            error: str,
            change: dict = None,
            item: Item = None,
            cash: Money = None,
    ):
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.trans_type = trans_type
        self.item = item
        self.cash = cash
        self.change = change
        self.result = result
        self.error = error
