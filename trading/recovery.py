from trading import Transaction, TradingBotBase


class Martingale:
    def __init__(self, trading_bot: TradingBotBase) -> None:        
        self.bot   = trading_bot
        self.setup = self.bot.setup

    def update_entry_value(self, value: float):
        self.setup.money_amount = value

    def get_next_entry(self) -> float:
        money_amount = self.setup.money_amount
        factor       = self.setup.factor
        return money_amount + money_amount * factor

    def run(self, transaction: Transaction):
        initial_amount = self.setup.money_amount
        
        for level in range(self.setup.martingales):
            self.update_entry_value(self.get_next_entry())

            print(f'** [{self.setup.asset}]: Martingale {level+1}')
            transaction = self.bot.perform_transaction(transaction.action)
            self.bot.update_profit(transaction)
            self.bot.verify_if_should_stop()

            if(transaction.profit > 0): break
        
        self.update_entry_value(initial_amount)
        