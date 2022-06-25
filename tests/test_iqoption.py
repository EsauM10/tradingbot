import pytest
from pytest import MonkeyPatch
from datetime import datetime
from trading.exceptions import TransactionCanceled
from trading.exchanges.iqoption import IQOptionExchange
from trading.util import Action, Candle, Transaction


def test_should_connect_with_correct_credentials(monkeypatch: MonkeyPatch):
    connect  = lambda: (True, '')
    exchange = IQOptionExchange(email='', password='')
    monkeypatch.setattr(exchange.api, 'connect', connect)
    assert exchange.connect() == True


def test_should_raises_an_exception_when_incorrect_credentials_is_passed(monkeypatch: MonkeyPatch):
    connect  = lambda: (False, '')
    exchange = IQOptionExchange(email='', password='')
    monkeypatch.setattr(exchange.api, 'connect', connect)
    with pytest.raises(Exception):
        exchange.connect()


def test_should_raises_an_exception_when_the_transaction_was_canceled(monkeypatch: MonkeyPatch):
    buy = lambda amount, asset, direction, expiration: (False, None)
    exchange = IQOptionExchange(email='', password='')
    monkeypatch.setattr(exchange.api, 'buy', buy)
    with pytest.raises(TransactionCanceled):
        exchange.buy(asset='', expiration=0, amount=0, action=None)
    

def test_should_return_a_transaction(monkeypatch: MonkeyPatch):
    buy = lambda amount, asset, direction, expiration: (True, 100)
    exchange = IQOptionExchange(email='', password='')
    monkeypatch.setattr(exchange.api, 'buy', buy)
    transaction = exchange.buy(asset='EURUSD', expiration=1, amount=2.0, action=Action.BUY)
    
    assert transaction.id == 100
    assert transaction.asset == 'EURUSD'
    assert transaction.expiration_time == 1
    assert transaction.money_amount == 2.0
    assert transaction.action == Action.BUY
    assert transaction.is_completed == False


def test_should_return_a_empty_candle_list_when_candles_amount_is_less_or_equal_to_zero():
    exchange = IQOptionExchange(email='', password='')
    candles1 = exchange.get_candles(asset='', timeframe=0, candles_amount=0, timestamp=0.0)
    candles2 = exchange.get_candles(asset='', timeframe=0, candles_amount=-10, timestamp=0.0)
    assert candles1 == []
    assert candles2 == []
    

def test_should_raises_an_exception_when_candles_amount_is_greater_than_1000():
    exchange = IQOptionExchange(email='', password='')
    with pytest.raises(Exception):
        exchange.get_candles(asset='', timeframe=0, candles_amount=1001, timestamp=0.0)


def test_should_return_a_candle_list(monkeypatch: MonkeyPatch):
    start_time = datetime.fromtimestamp(0)
    end_time   = datetime.fromtimestamp(60)

    data = [
        {'id': 0, 'open': 0.988586, 'close': 0.988608, 'max': 0.988615, 'min': 0.988547, 'volume': 15, 'from': 0, 'to': 60},
        {'id': 1, 'open': 0.988611, 'close': 0.988563, 'max': 0.988624, 'min': 0.988523, 'volume': 12, 'from': 0, 'to': 60},
        {'id': 2, 'open': 0.988562, 'close': 0.988651, 'max': 0.988664, 'min': 0.988557, 'volume': 18, 'from': 0, 'to': 60}
    ]
    expected_candles = [
        Candle(id=0, open=0.988586, close=0.988608, high=0.988615, low=0.988547, volume=15, start_time=start_time, end_time=end_time),
        Candle(id=1, open=0.988611, close=0.988563, high=0.988624, low=0.988523, volume=12, start_time=start_time, end_time=end_time),
        Candle(id=2, open=0.988562, close=0.988651, high=0.988664, low=0.988557, volume=18, start_time=start_time, end_time=end_time)
    ]

    get_candles = lambda asset, timeframe, amount, timestamp: data
    exchange = IQOptionExchange(email='', password='')
    monkeypatch.setattr(exchange.api, 'get_candles', get_candles)
    candles = exchange.get_candles(asset='', timeframe=0, candles_amount=3, timestamp=0)
    assert candles == expected_candles
    

def test_should_wait_until_the_transaction_status_is_completed(monkeypatch: MonkeyPatch):
    check_win = lambda id: ('win', 1.0)
    exchange = IQOptionExchange(email='', password='')
    monkeypatch.setattr(exchange.api, 'check_win_v4', check_win)

    transaction = Transaction(id=0, asset='', expiration_time=0, money_amount=0, action=None)
    exchange.wait_transaction(transaction)
    
    assert transaction.is_completed == True
    assert transaction.profit == 1.0