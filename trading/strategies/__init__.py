from abc import ABC, abstractmethod
from trading.util import Action, Candle


class TradingStrategy(ABC):
    def __init__(self, candles_amount:int) -> None:
        super().__init__()
        self.candles_amount = candles_amount

    @abstractmethod
    def evaluate(self, candles: list[Candle])-> Action:
        pass