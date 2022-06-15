import pytest
from trading.exceptions import StopTradingBot
from trading.strategies.prices import PriceAlert, PriceMonitorStrategy
from trading.util import Action, Candle

candles = [
    Candle(
        open=0.988500, 
        close=0.988600, 
        high=0.988615, 
        low=0.988547, 
        volume=15, 
        start_time=None, 
        end_time=None
    )
]

def test_should_raises_a_exception_when_alerts_is_empty():
    strategy = PriceMonitorStrategy(alerts=[])
    with pytest.raises(StopTradingBot):
        strategy.evaluate(candles=candles)

def test_should_hold_if_the_price_not_is_reached():
    strategy = PriceMonitorStrategy(
        alerts=[
            PriceAlert(price=0.988400, action=Action.BUY),
        ]
    )
    result = strategy.evaluate(candles=candles)
    assert result == Action.HOLD


def test_should_buy_if_the_price_is_reached():
    strategy = PriceMonitorStrategy(
        alerts=[
            PriceAlert(price=0.988600, action=Action.BUY),
        ]
    )
    result = strategy.evaluate(candles=candles)
    assert result == Action.BUY


def test_should_sell_if_the_price_is_reached():
    strategy = PriceMonitorStrategy(
        alerts=[
            PriceAlert(price=0.988600, action=Action.SELL),
        ]
    )
    result = strategy.evaluate(candles=candles)
    assert result == Action.SELL



