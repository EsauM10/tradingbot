class TradingSetup:
    def __init__(self, asset:str, timeframe:int, money_amount:float, 
        stoploss:float, stopgain: float,
    ) -> None:
        self.asset          = asset
        self.timeframe      = timeframe
        self.money_amount   = money_amount
        self.stoploss       = stoploss
        self.stopgain       = stopgain