from enum import Enum


class TransType(Enum):
    """Class with list of transaction type prompts"""

    CUSTOMER_ADD_CASH = "Внесение наличных покупателем"
    CUSTOMER_BUY_ITEM = "Покупка товара покупателем"
    CUSTOMER_GIVE_CHANGE = "Выдача сдачи покупателю"
    MERCHANT_ADD_CASH = "Внесение наличных торговцем"
    MERCHANT_ADD_ITEM = "Внесение товара торговцем"
    MERCHANT_REMOVE_ITEM = "Изъятие товара торговцем"
    MERCHANT_WITHDRAW = "Изъятие наличных торговцем"
