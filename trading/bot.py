import time
from trading import TradingBotBase
from trading.util import Action, Transaction
from trading.exceptions import HoldAction, StopLossReached, StopGainReached, TransactionCanceled, StopTradingBot
from trading.exchanges import Exchange
from trading.recovery import Martingale, Soros
from trading.strategies import TradingStrategy
from trading.setup import TradingSetup
    
class TradingBot(TradingBotBase):
    def __init__(self, exchange: Exchange, setup: TradingSetup, strategy: TradingStrategy):
        self.exchange      = exchange
        self.setup         = setup
        self.strategy      = strategy
        self.time_interval = 0.5
        self._running      = False
        self._profit       = 0.0

        self.martingale    = Martingale(trading_bot=self)
        self.soros         = Soros(trading_bot=self)

    @property
    def profit(self):
        return self._profit


    def do_martingale(self, transaction: Transaction):
        if(transaction.profit >= 0 or self.setup.martingales <= 0): return
        self.martingale.run(transaction)

    def do_soros(self, transaction: Transaction):
        if(transaction.profit <= 0 or self.setup.soros <= 0): return
        self.soros.run(transaction)

    def perform_transaction(self, action: Action) -> Transaction:
        asset      = self.setup.asset
        amount     = self.setup.money_amount
        expiration = self.setup.timeframe

        if(action == Action.HOLD):
            raise HoldAction()
        if(action == Action.BUY):
            return self.exchange.buy(asset, expiration, amount)
        if(action == Action.SELL):
            return self.exchange.sell(asset, expiration, amount)

    def update_profit(self, transaction: Transaction):
        self._profit += transaction.profit

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
                result      = self.strategy.evaluate(candles=candles)
                transaction = self.perform_transaction(action=result)
                
                self.update_profit(transaction)
                self.do_soros(transaction)
                self.do_martingale(transaction)
                self.verify_if_should_stop()

            except HoldAction: pass
            except TransactionCanceled as ex: 
                print(ex)
            except (StopGainReached, StopLossReached, StopTradingBot):
                self.stop()
                
            time.sleep(self.time_interval)

    
    def stop(self):
        self._running = False
