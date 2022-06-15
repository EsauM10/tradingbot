import numpy as np
from numpy import ndarray
from trading.util import Candle

def filter_data_by(data: list[Candle], key:str) -> ndarray:
    '''Filtra os dados de uma lista de Candle por uma key especifica''' 
    return np.array([
        item.to_dict[key] 
        for item in data if key in item.to_dict
    ])

def get_dataset(candles: list[Candle], keys: list[str]) -> dict[str, ndarray]:
    '''Retorna um dataset agrupado por uma lista de keys'''
    return {
        key: filter_data_by(candles, key) 
        for key in keys
    }