from typing import Literal
from trading.exceptions import StopTradingBot
from trading.helpers import get_max_price, get_min_price
from trading.strategies import TradingStrategy
from trading.util import Action, Candle

FibonacciLevels = Literal['23.6', '38.2', '50', '61.8', '100']

class Level:
    def __init__(self, level: FibonacciLevels) -> None:
        self.level = level
    
    def get_fibonacci_price(self, max_price: float, min_price: float) -> float:
        level = float(self.level) / 100
        interval = max_price - min_price
        return round(max_price - interval * level, 6)

    def __repr__(self) -> str:
        return f'Level(level={self.level}%)'


class FibonacciStrategy(TradingStrategy):
    def __init__(self, levels: list[Level], candles_amount: int = 100) -> None:
        super().__init__(candles_amount)
        self.levels = levels
        print(f'** Levels: {self.levels}\n')

    def price_reached_level(self, price: float, target_price: float) -> bool:
        return  0.999985 < (price / target_price) < 1.000015

    def purchase_on_reversion(self, candle: Candle) -> Action:
        return Action.BUY if(candle.color() == 'RED') else Action.SELL
        
    def evaluate(self, candles: list[Candle]) -> Action:
        if(not self.levels): raise StopTradingBot()

        max_price   = get_max_price(candles, price_type='high')
        min_price   = get_min_price(candles, price_type='low')
        last_candle = candles[-1]
        price       = last_candle.close
        print(f'Preço atual: {price} | Max: {max_price} | Min: {min_price} ', end='\r')

        for level in self.levels:
            target_price = level.get_fibonacci_price(max_price, min_price)
            if(self.price_reached_level(price, target_price)):
                self.levels.remove(level)
                return self.purchase_on_reversion(candle=last_candle)
        
        return Action.HOLD