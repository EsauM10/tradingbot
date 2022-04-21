from abc import ABC, abstractmethod
from trading.util import Action, Transaction


class TradingBotBase(ABC):
    
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