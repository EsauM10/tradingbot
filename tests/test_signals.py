import pytest, time
from pytest import MonkeyPatch
from datetime import datetime
from trading.exceptions import StopTradingBot, TransactionCanceled
from trading.setup import TradingSetup
from trading.strategies.signals import DATE_FORMAT, Entry, ListOfSignalsStrategy
from trading.util import Action


def test_should_parse_a_entry_string():
    entry_string = '15/04;17:00;NZDUSD-OTC;M5;PUT'
    entry = Entry(entry_string)
    expected_date = datetime.strptime(f'15/04/{datetime.now().year} 17:00', DATE_FORMAT)

    assert entry.asset == 'NZDUSD-OTC'
    assert entry.timeframe == 5
    assert entry.action == Action.SELL
    assert entry.target_hour == expected_date


def test_should_return_true_if_string_matches_a_pattern():
    strategy = ListOfSignalsStrategy([], setup=None)
    result   = strategy.matches(entry='15/04;17:06;USDCHF;M1;PUT')
    assert result == True

def test_should_return_false_if_string_do_not_matches_a_pattern():
    strategy = ListOfSignalsStrategy([], setup=None)
    result   = strategy.matches(entry='15/04]17:32;EURUSD;M1;PUT')
    assert result == False


def test_should_parse_a_string_list():
    string_list = [
        '15/04;17:00;NZDUSD-OTC;M5;PUTS',
        '15/04;17:06;USDCHF;M1;PUT',
        '15/04]17:32;EURUSD;M1;CALL',
        '15/04;17:08;AUDCAD;M1;PUT',
    ]
    reversed_entries = [
        Entry('15/04;17:08;AUDCAD;M1;PUT'),
        Entry('15/04;17:06;USDCHF;M1;PUT'),
    ]
    strategy = ListOfSignalsStrategy([], setup=None)
    entries  = strategy.parse_data(entries=string_list)
    assert entries == reversed_entries


def test_should_raises_a_exception_when_entries_is_empty():
    strategy = ListOfSignalsStrategy([], setup=None)
    with pytest.raises(StopTradingBot):
        strategy.evaluate(candles=[])


def test_should_raises_a_exception_when_the_entry_remaining_time_is_negative(monkeypatch: MonkeyPatch):
    setup = TradingSetup(asset='', timeframe=0, money_amount=0, stoploss=0, stopgain=0)
    strategy = ListOfSignalsStrategy(['15/04;17:06;USDCHF;M1;PUT'], setup)

    entry = strategy.entries[0]
    add_one_minute_from_entry_hour = lambda : entry.target_hour.timestamp() + 60
    monkeypatch.setattr(time, 'time', add_one_minute_from_entry_hour)
    
    with pytest.raises(TransactionCanceled):
        strategy.evaluate(candles=[])
    

def test_should_buy_when_a_buy_entry_is_passed(monkeypatch: MonkeyPatch):
    setup = TradingSetup(asset='', timeframe=0, money_amount=0, stoploss=0, stopgain=0)
    strategy = ListOfSignalsStrategy(
        entries=[
            '15/04;17:06;EURUSD;M1;CALL',
            '15/04;17:04;EURUSD;M5;PUT'
        ], 
        setup=setup)

    entry = strategy.entries[-1]
    subtract_one_minute_from_entry_hour = lambda : entry.target_hour.timestamp() - 60
    monkeypatch.setattr(time, 'time', subtract_one_minute_from_entry_hour)
    monkeypatch.setattr(time, 'sleep', lambda secs: 0)

    action = strategy.evaluate(candles=[])
    assert action == Action.BUY


def test_should_sell_when_a_sell_entry_is_passed(monkeypatch: MonkeyPatch):
    setup = TradingSetup(asset='', timeframe=0, money_amount=0, stoploss=0, stopgain=0)
    strategy = ListOfSignalsStrategy(['15/04;17:06;EURUSD;M1;PUT'], setup)

    entry = strategy.entries[0]
    subtract_one_minute_from_entry_hour = lambda : entry.target_hour.timestamp() - 60
    monkeypatch.setattr(time, 'time', subtract_one_minute_from_entry_hour)
    monkeypatch.setattr(time, 'sleep', lambda secs: 0)

    action = strategy.evaluate(candles=[])
    assert action == Action.SELL