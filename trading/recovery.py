from trading import Transaction, TradingBotBase


class Martingale:
    def __init__(self, trading_bot: TradingBotBase) -> None:        
        self.bot   = trading_bot
        self.setup = self.bot.setup
        self.__initial_entry_value = self.setup.money_amount


    def __update_entry_value(self):
        self.setup.money_amount += self.setup.money_amount * self.setup.factor

    def __reset_entry_value(self):
        self.setup.money_amount = self.__initial_entry_value

    def run(self, transaction: Transaction):
        for level in range(self.setup.martingales):
            self.__update_entry_value()

            print(f'** [{self.setup.asset}]: Martingale {level+1}')
            transaction = self.bot.perform_transaction(transaction.action)
            self.bot.update_profit(transaction)
            self.bot.verify_if_should_stop()

            if(transaction.profit > 0): break
        
        self.__reset_entry_value()