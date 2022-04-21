from random import randint
from trading.util import Action, Candle
from trading.strategies import TradingStrategy

class RandomStrategy(TradingStrategy):
    def __init__(self) -> None:
        super().__init__(candles_amount=0)
    
    def evaluate(self, candles: list[Candle]) -> Action:
        number = randint(0, 1)
        if(number): return Action.BUY
        return Action.SELL
