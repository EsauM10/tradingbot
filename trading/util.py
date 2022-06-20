from datetime import datetime
from enum import Enum, auto

class Action(Enum):
    BUY = auto()
    SELL = auto()
    HOLD = auto()

class Color(Enum):
    GREEN = 'green'
    RED   = 'red'
    GREY  = 'grey'


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
    
    @property
    def color(self) -> Color:
        if(self.close > self.open): return Color.GREEN
        if(self.close < self.open): return Color.RED
        return Color.GREY

    def __repr__(self) -> str:
        start = self.start_time.strftime('%H:%M')
        end   = self.end_time.strftime('%H:%M')
        return f'Candle(color={self.color.value}, start={start}, end={end})'
    
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