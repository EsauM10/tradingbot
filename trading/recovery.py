from abc import ABC, abstractmethod
from trading.setup import TradingSetup
from trading.util import Transaction


class RecoveryStrategy(ABC):
    def __init__(self, count: int) -> None:
        self.count = count
    
    @abstractmethod
    def calculate(self, setup: TradingSetup, transaction: Transaction) -> float:
        pass
    
    @abstractmethod
    def should_stop(self, transaction: Transaction) -> bool:
        pass


class Martingale(RecoveryStrategy):
    def __init__(self, count: int) -> None:
        super().__init__(count)

    def calculate(self, setup: TradingSetup, transaction: Transaction) -> float:
        money_amount = setup.money_amount
        factor       = setup.factor
        return money_amount + money_amount * factor

    def should_stop(self, transaction: Transaction) -> bool:
        return transaction.profit > 0

    def __str__(self) -> str:
        return 'Martingale'


class Soros(RecoveryStrategy):
    def __init__(self, count: int) -> None:
        super().__init__(count)

    def calculate(self, setup: TradingSetup, transaction: Transaction):
        return setup.money_amount + transaction.profit
    
    def should_stop(self, transaction: Transaction) -> bool:
        return transaction.profit < 0

    def __str__(self) -> str:
        return 'Soros'
