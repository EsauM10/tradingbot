import numpy as np
from abc import ABC, abstractmethod
from trading import Action, Candle



class TradingStrategy(ABC):
    def __init__(self, candles_amount:int) -> None:
        super().__init__()
        self.candles_amount = candles_amount

    @abstractmethod
    def evaluate(self, candles: list[Candle])-> Action:
        pass
    
    def filter_data_by(self, data: list[Candle], key:str):
        '''Filtra os dados de uma lista de Candle por uma key especifica''' 
        return np.array([item.to_dict[key] for item in data if key in item.to_dict])

    def get_dataset(self, candles: list[Candle], keys: list[str]):
        '''Retorna um dataset agrupado por uma lista de keys'''
        return {key: self.filter_data_by(candles, key) for key in keys}