from typing import Callable
from trading import Action, Candle
from trading.exceptions import StopTradingBot
from trading.strategies import TradingStrategy


class PriceAlert:
    def __init__(self, price: float, action: Action) -> None:
        self.price  = price
        self.action = action
        self.should_purchase = self.__get_purchase_condition()
    
    def __get_purchase_condition(self) -> Callable[[float], bool]:
        if(self.action == Action.BUY):
            return lambda price: price <= self.price

        return lambda price: price >= self.price

    def __repr__(self) -> str:
        return f'Alert(price={self.price}, {self.action.name})'
    

class PriceMonitorStrategy(TradingStrategy):
    def __init__(self, alerts: list[PriceAlert]) -> None:
        super().__init__(candles_amount=1)
        self.alerts = alerts
        print(f'** Alertas: {self.alerts}')

    def remove_alert(self, alert: PriceAlert):
        self.alerts.remove(alert)

    def evaluate(self, candles: list[Candle]) -> Action:
        if(not self.alerts): raise StopTradingBot()

        price = candles[-1].close
        print(f'Preço atual: {price}', end='\r')

        for alert in self.alerts:
            if(alert.should_purchase(price)):
                self.remove_alert(alert)
                return alert.action
        
        return Action.HOLD