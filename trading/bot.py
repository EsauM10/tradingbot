import time
from trading.util import Action, Transaction
from trading.exceptions import HoldAction, StopLossReached, StopGainReached, TransactionCanceled, StopTradingBot
from trading.exchanges import Exchange
from trading.recovery import Martingale, RecoveryStrategy, Soros
from trading.strategies import TradingStrategy
from trading.setup import TradingSetup
    
class TradingBot:
    def __init__(self, exchange: Exchange, setup: TradingSetup, strategy: TradingStrategy):
        self.exchange      = exchange
        self.setup         = setup
        self.strategy      = strategy
        self.time_interval = 0.5
        self._running      = False
        self._profit       = 0.0

    @property
    def profit(self):
        return self._profit

    def repeat_transaction(self, transaction: Transaction, recovery: RecoveryStrategy):
        initial_amount = self.setup.money_amount
        
        for level in range(recovery.count):
            print(f'** [{self.setup.asset}]: {recovery} {level+1}')
            money_amount = recovery.calculate(self.setup, transaction)
            self.setup.set_money(money_amount)
             
            transaction = self.perform_transaction(transaction.action)
            self.update_profit(transaction)
            self.verify_if_should_stop()

            if(recovery.should_stop(transaction)): break
        self.setup.set_money(initial_amount)
    

    def do_martingale(self, transaction: Transaction):
        martingale = Martingale(count=self.setup.martingales)
        self.repeat_transaction(transaction, recovery=martingale)

    def do_soros(self, transaction: Transaction):
        soros = Soros(count=self.setup.soros)
        self.repeat_transaction(transaction, recovery=soros)


    def perform_transaction(self, action: Action) -> Transaction:
        asset      = self.setup.asset
        amount     = self.setup.money_amount
        expiration = self.setup.timeframe

        if(action == Action.HOLD):
            raise HoldAction()
        
        transaction = self.exchange.buy(asset, expiration, amount, action)
        print(f'** [{asset}]: Operacao iniciada   -> {action.name}')
        self.exchange.wait_transaction(transaction)
        print(f'** [{asset}]: Operacao finalizada -> {transaction}\n')
        return transaction


    def update_profit(self, transaction: Transaction):
        self._profit += transaction.profit
    
    def should_do_martingale(self, transaction: Transaction) -> bool:
        return transaction.profit < 0 and self.setup.martingales > 0
    
    def should_do_soros(self, transaction: Transaction) -> bool:
        return transaction.profit > 0 and self.setup.soros > 0

    def stoploss_was_reached(self) -> bool:
        return self.profit <= -self.setup.stoploss
    
    def stopgain_was_reached(self) -> bool:
        return self.profit >= self.setup.stopgain

    def verify_if_should_stop(self):
        if(self.stoploss_was_reached()): 
            raise StopLossReached('** Stop Loss atingido')
        if(self.stopgain_was_reached()):
            raise StopGainReached('** Stop Win atingido')
    

    def run(self):
        asset          = self.setup.asset
        timeframe      = self.setup.timeframe
        candles_amount = self.strategy.candles_amount
        self._running  = True

        while self._running:
            try:  
                candles     = self.exchange.get_candles(asset, timeframe, candles_amount, timestamp=time.time())
                action      = self.strategy.evaluate(candles=candles)
                transaction = self.perform_transaction(action=action)
                
                self.update_profit(transaction)
                self.verify_if_should_stop()

                if(self.should_do_soros(transaction)):
                    self.do_soros(transaction)
                elif(self.should_do_martingale(transaction)):
                    self.do_martingale(transaction)
                
                
            except HoldAction: pass
            except TransactionCanceled as ex: 
                print(ex)
            except (StopGainReached, StopLossReached, StopTradingBot):
                self.stop()
                
            time.sleep(self.time_interval)

    
    def stop(self):
        self._running = False
