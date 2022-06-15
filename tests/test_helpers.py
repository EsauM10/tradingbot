import pytest
import numpy as np
import trading.helpers as helpers
from datetime import datetime, timedelta
from trading.util import Candle

start_time = datetime.now() - timedelta(minutes=1)
end_time   = datetime.now()

candles = [
    Candle(open=0.988586, close=0.988608, high=0.988615, low=0.988547, volume=15, start_time=start_time, end_time=end_time),
    Candle(open=0.988611, close=0.988563, high=0.988624, low=0.988523, volume=12, start_time=None, end_time=None),
    Candle(open=0.988562, close=0.988651, high=0.988664, low=0.988557, volume=18, start_time=None, end_time=None),
    Candle(open=0.988651, close=0.988675, high=0.988701, low=0.988571, volume=16, start_time=None, end_time=None),
    Candle(open=0.988658, close=0.988725, high=0.988756, low=0.988658, volume=14, start_time=None, end_time=None),
    Candle(open=0.988721, close=0.988701, high=0.988768, low=0.988685, volume=19, start_time=None, end_time=None),
]


def test_should_return_a_empty_array_when_an_empty_list_is_passed():
    result = helpers.filter_data_by(data=[], key='close')
    assert result.size == 0

def test_should_return_a_empty_array_when_an_invalid_key_is_passed():
    result = helpers.filter_data_by(data=candles, key='any')
    assert result.size == 0

def test_should_filter_data_by_close_prices():
    expected_prices = np.array([0.988608, 0.988563, 0.988651, 0.988675, 0.988725, 0.988701])
    result = helpers.filter_data_by(data=candles, key='close')
    assert (result == expected_prices).all()

def test_should_filter_data_by_open_prices():
    expected_prices = np.array([0.988586, 0.988611, 0.988562, 0.988651, 0.988658, 0.988721])
    result = helpers.filter_data_by(data=candles, key='open')
    assert (result == expected_prices).all()

def test_should_filter_data_by_high_prices():
    expected_prices = np.array([0.988615, 0.988624, 0.988664, 0.988701, 0.988756, 0.988768])
    result = helpers.filter_data_by(data=candles, key='high')
    assert (result == expected_prices).all()

def test_should_filter_data_by_low_prices():
    expected_prices = np.array([0.988547, 0.988523, 0.988557, 0.988571, 0.988658, 0.988685])
    result = helpers.filter_data_by(data=candles, key='low')
    assert (result == expected_prices).all()

def test_should_filter_data_by_volume():
    expected = np.array([15, 12, 18, 16, 14, 19])
    result = helpers.filter_data_by(data=candles, key='volume')
    assert (result == expected).all()




def test_should_raises_a_exception_when_invalid_price_key_is_passed():
    with pytest.raises(KeyError):
        helpers.get_max_price(candles, price_type='any')
        helpers.get_min_price(candles, price_type='any')

def test_should_return_the_higher_price():
    high_prices = helpers.filter_data_by(data=candles, key='high')
    expected = max(high_prices)
    result   = helpers.get_max_price(candles, price_type='high')
    assert result == expected

def test_should_return_the_lower_price():
    low_prices = helpers.filter_data_by(data=candles, key='low')
    expected = min(low_prices)
    result   = helpers.get_min_price(candles, price_type='low')
    assert result == expected