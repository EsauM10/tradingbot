import pytest
from trading.exceptions import StopTradingBot
from trading.strategies.fibonacci import FibonacciStrategy, Level
from trading.util import Action, Candle

fibonacci_levels = ['23.6', '38.2', '50', '61.8']

candles = [
    Candle(open=0.909094, close=0.909093, high=0.909128, low=0.909081, volume=0, start_time=None, end_time=None),
    Candle(open=0.909097, close=0.909035, high=0.9091,   low=0.909025, volume=0, start_time=None, end_time=None),
    Candle(open=0.909033, close=0.908978, high=0.909085, low=0.908978, volume=0, start_time=None, end_time=None),
    Candle(open=0.908976, close=0.909015, high=0.909027, low=0.90897,  volume=0, start_time=None, end_time=None),
    Candle(open=0.909018, close=0.908818, high=0.909037, low=0.908818, volume=0, start_time=None, end_time=None),
    Candle(open=0.908815, close=0.908886, high=0.908892, low=0.908773, volume=0, start_time=None, end_time=None),
    Candle(open=0.908885, close=0.90874,  high=0.908886, low=0.90874,  volume=0, start_time=None, end_time=None),
    Candle(open=0.908738, close=0.908786, high=0.908804, low=0.908726, volume=0, start_time=None, end_time=None),
    Candle(open=0.908797, close=0.908821, high=0.908884, low=0.908786, volume=0, start_time=None, end_time=None),
    Candle(open=0.908822, close=0.908712, high=0.908834, low=0.908712, volume=0, start_time=None, end_time=None),
    Candle(open=0.908738, close=0.908768, high=0.908785, low=0.908714, volume=0, start_time=None, end_time=None),
    Candle(open=0.908771, close=0.908632, high=0.908773, low=0.908625, volume=0, start_time=None, end_time=None),
    Candle(open=0.908632, close=0.908641, high=0.908663, low=0.90861,  volume=0, start_time=None, end_time=None),
    Candle(open=0.908616, close=0.908648, high=0.908668, low=0.908589, volume=0, start_time=None, end_time=None),
    Candle(open=0.90865,  close=0.90871,  high=0.908718, low=0.908633, volume=0, start_time=None, end_time=None),
    Candle(open=0.908712, close=0.908742, high=0.908753, low=0.908683, volume=0, start_time=None, end_time=None),
]



def test_should_calculate_price_for_all_fibonacci_levels():
    max_price = 0.910626
    min_price = 0.909234
    
    expected_prices  = [0.910297, 0.910094, 0.90993, 0.909766]
    fibonacci_prices = [
        Level(level=level).get_fibonacci_price(max_price, min_price) 
        for level in fibonacci_levels
    ]
    assert fibonacci_prices == expected_prices


def test_should_return_true_if_the_price_reached_the_level():
    strategy = FibonacciStrategy(levels=[])
    
    level1 = strategy.price_reached_level(price=0.910612, target_price=0.910625)
    level2 = strategy.price_reached_level(price=0.910638, target_price=0.910625)
    assert level1 == True
    assert level2 == True


def test_should_return_false_if_the_price_not_reached_the_level():
    strategy = FibonacciStrategy(levels=[])
    
    level1 = strategy.price_reached_level(price=0.910610, target_price=0.910625)
    level2 = strategy.price_reached_level(price=0.910640, target_price=0.910625)
    assert level1 == False
    assert level2 == False


def test_should_buy_when_the_price_falls():
    red_candle = Candle(
        open=0.988500, 
        close=0.988400,
        high=0.988615, 
        low=0.988547, 
        volume=15, 
        start_time=None, 
        end_time=None
    )
    strategy = FibonacciStrategy(levels=[])
    action = strategy.purchase_on_reversion(candle=red_candle)
    assert action == Action.BUY


def test_should_sell_when_the_price_grows():
    green_candle = Candle(
        open=0.988500, 
        close=0.988600,
        high=0.988615, 
        low=0.988547, 
        volume=15, 
        start_time=None, 
        end_time=None
    )
    strategy = FibonacciStrategy(levels=[])
    action = strategy.purchase_on_reversion(candle=green_candle)
    assert action == Action.SELL


def test_should_raises_an_exception_when_levels_is_empty():
    strategy = FibonacciStrategy(levels=[])
    with pytest.raises(StopTradingBot):
        strategy.evaluate(candles=[])


def test_should_hold_if_the_price_not_reached_any_level():
    levels = [
        Level(level='23.6'),
        Level(level='38.2'),
        Level(level='50'),
        Level(level='61.8')
    ]
    strategy = FibonacciStrategy(levels=levels)
    action = strategy.evaluate(candles=candles)
    assert action == Action.HOLD


def test_should_purchase_in_all_fibonacci_level():
    candles_to_append = [
        Candle(open=0.909060, close=0.908990, high=0.909070, low=0.909001, volume=0, start_time=None, end_time=None),
        Candle(open=0.908858, close=0.908930, high=0.908940, low=0.908850, volume=0, start_time=None, end_time=None),
        Candle(open=0.908808, close=0.908858, high=0.908870, low=0.908790, volume=0, start_time=None, end_time=None),
        Candle(open=0.908830, close=0.908808, high=0.908845, low=0.908795, volume=0, start_time=None, end_time=None),
    ]

    levels = [
        Level(level='23.6'),
        Level(level='38.2'),
        Level(level='50'),
        Level(level='61.8'),
    ]
    strategy = FibonacciStrategy(levels=levels)

    expected_actions = [Action.BUY, Action.SELL, Action.SELL, Action.BUY]
    actions = []
    
    while(candles_to_append):
        candles.append(candles_to_append.pop())
        action = strategy.evaluate(candles=candles)
        actions.append(action)

    assert actions == expected_actions
