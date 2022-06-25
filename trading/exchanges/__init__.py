from abc import ABC, abstractmethod

from trading.util import Action, Candle, Transaction


class Exchange(ABC):

    @abstractmethod
    def connect(self) -> bool:
        pass
    
    @abstractmethod
    def buy(self, asset:str, expiration:int, amount:float, action: Action) -> Transaction:
        pass
    
    @abstractmethod
    def get_candles(self, asset: str, timeframe:int, candles_amount:int, timestamp:float) -> list[Candle]:
        pass

    @abstractmethod
    def wait_transaction(self, transaction: Transaction):
        pass
