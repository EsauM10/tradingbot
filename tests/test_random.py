from pytest import MonkeyPatch
from trading.strategies.random import RandomStrategy, random
from trading.util import Action


def test_should_buy_when_a_positive_value_is_raffled(monkeypatch: MonkeyPatch):
    monkeypatch.setattr(random, 'randint', lambda x, y: 1)
    strategy = RandomStrategy()
    result   = strategy.evaluate(candles=[])
    assert result == Action.BUY


def test_should_sell_when_a_zero_value_is_raffled(monkeypatch: MonkeyPatch):
    monkeypatch.setattr(random, 'randint', lambda x, y: 0)
    strategy = RandomStrategy()
    result   = strategy.evaluate(candles=[])
    assert result == Action.SELL