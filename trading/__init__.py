from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum, auto


class Action(Enum):
    BUY = auto()
    SELL = auto()
    HOLD = auto()


class Candle:
    def __init__(self, 
        open:float, close: float, high: float, low: float, 
        volume:int, start_time:datetime, end_time: datetime
    ) -> None:
        self.open   = open
        self.close  = close
        self.high   = high
        self.low    = low
        self.volume = volume
        self.start_time = start_time
        self.end_time = end_time
    
    def color(self)->str:
        if(self.close > self.open): return 'GREEN'
        if(self.close < self.open): return 'RED'
        return 'GRAY'

    def __repr__(self) -> str:
        start = self.start_time.strftime('%H:%M')
        end   = self.end_time.strftime('%H:%M')
        return f'Candle(color={self.color()}, start={start}, end={end})'
    
    @property
    def to_dict(self):
        return {
            'open': self.open,
            'close': self.close,
            'high': self.high,
            'low': self.low,
            'volume': self.volume,
            'start_time': self.start_time,
            'end_time': self.end_time
        }


class Transaction:
    def __init__(self, result:str, profit:float) -> None:
        self.result = result
        self.profit = profit
        self.action = None
    
    def __str__(self) -> str:
        return f'<result={self.result}, profit={self.profit}>'


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