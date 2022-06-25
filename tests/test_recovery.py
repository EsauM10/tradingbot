from trading.recovery import Martingale, Soros
from trading.setup import TradingSetup
from trading.util import Transaction

# ============================= Martingale ============================= #
def test_should_double_next_entry_value_for_martingale():
    martingale = Martingale(count=0)
    setup      = TradingSetup(asset='', timeframe='', money_amount=2.0, factor=1.0, stoploss=0.0, stopgain=0.0) 
    result     = martingale.calculate(setup=setup, transaction=None)
    assert result == 4.0


def test_should_stop_martingale_if_profit_is_positive():
    martingale  = Martingale(count=0)
    transaction = Transaction(id=0, asset='', expiration_time=0, money_amount=0, action=None)
    transaction.profit = 1.0
    result      = martingale.should_stop(transaction=transaction)
    assert result == True


def test_should_continue_martingale_if_profit_is_negative():
    martingale  = Martingale(count=0)
    transaction = Transaction(id=0, asset='', expiration_time=0, money_amount=0, action=None)
    transaction.profit = -1.0
    result      = martingale.should_stop(transaction=transaction)
    assert result == False

def test_should_continue_martingale_if_profit_is_zero():
    martingale  = Martingale(count=0)
    transaction = Transaction(id=0, asset='', expiration_time=0, money_amount=0, action=None)
    result      = martingale.should_stop(transaction=transaction)
    assert result == False

# =============================== Soros =============================== #
def test_should_sum_the_profit_with_the_initial_money_for_soros():
    soros       = Soros(count=0)
    transaction = Transaction(id=0, asset='', expiration_time=0, money_amount=0, action=None)
    transaction.profit = 1.0
    setup       = TradingSetup(asset='', timeframe='', money_amount=2.0, stoploss=0.0, stopgain=0.0)
    result      = soros.calculate(setup=setup, transaction=transaction)
    assert result == 3.0

def test_should_stop_soros_if_profit_is_negative():
    soros       = Soros(count=0)
    transaction = Transaction(id=0, asset='', expiration_time=0, money_amount=0, action=None)
    transaction.profit = -1.0
    result      = soros.should_stop(transaction=transaction)
    assert result == True


def test_should_continue_soros_if_profit_is_positive():
    soros       = Soros(count=0)
    transaction = Transaction(id=0, asset='', expiration_time=0, money_amount=0, action=None)
    transaction.profit = 1.0
    result      = soros.should_stop(transaction=transaction)
    assert result == False


def test_should_continue_soros_if_profit_is_zero():
    soros       = Soros(count=0)
    transaction = Transaction(id=0, asset='', expiration_time=0, money_amount=0, action=None)
    result      = soros.should_stop(transaction=transaction)
    assert result == False