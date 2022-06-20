class Customer:
    def __init__(self, wallet: Wallet):
        self.wallet = wallet

    def get_wallet(self):
        return self.wallet

class Wallet:
    def __init__(self):
        self.money = 0

    def add_money(self, value: float):
        self.money += value

    def get_money(self):
        return Money(money=self.money)

class Money:
    def __init__(self, value: float):
        self.value = value

class AccountsReceviable:
    def __init__(self):
        pass

    def record_sale(self):
        pass

class Goods:
    def __init__(self, ar: AccountsReceviable):
        self.ar = ar

    def purchase(cust: Customer):
        self.cust.get_wallet().get_money()