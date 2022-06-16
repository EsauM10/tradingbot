from trading.util import Action, Candle
from trading.exceptions import StopTradingBot
from trading.strategies import TradingStrategy


class PriceAlert:
    def __init__(self, price: float, action: Action) -> None:
        self.target_price = price
        self.action = action
    
    def should_purchase(self, price: float) -> bool:
        return  0.999980 < (price / self.target_price) < 1.000020

    def __repr__(self) -> str:
        return f'Alert(price={self.target_price}, {self.action.name})'
    

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