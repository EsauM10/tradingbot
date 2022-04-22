from abc import ABC, abstractmethod
from trading.exchanges import Exchange
from trading.setup import TradingSetup
from trading.strategies import TradingStrategy
from trading.util import Action, Transaction


class TradingBotBase(ABC):
    def __init__(self, exchange: Exchange, setup: TradingSetup, strategy: TradingStrategy):
        self.exchange      = exchange
        self.setup         = setup
        self.strategy      = strategy
        
    @abstractmethod
    def perform_transaction(self, action: Action) -> Transaction:
        pass
    
    @abstractmethod
    def run(self):
        pass
    
    @abstractmethod
    def update_profit(self, transaction: Transaction):
        pass

    @abstractmethod
    def verify_if_should_stop(self):
        pass