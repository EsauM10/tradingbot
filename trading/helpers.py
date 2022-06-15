import numpy as np
from numpy import ndarray
from trading.util import Candle

PRICE_KEYS = ['high', 'low', 'open', 'close']

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


def get_max_price(candles: list[Candle], price_type: str) -> float:
    if(not price_type in PRICE_KEYS):
        raise KeyError(f'Informe uma key valida: {PRICE_KEYS}')

    data = filter_data_by(data=candles, key=price_type)
    return float(data.max())


def get_min_price(candles: list[Candle], price_type: str) -> float:
    if(not price_type in PRICE_KEYS):
        raise Exception(f'Informe uma key valida: {PRICE_KEYS}')
    
    data = filter_data_by(data=candles, key=price_type)
    return float(data.min())