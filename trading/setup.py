class TradingSetup:
    def __init__(self, asset:str, timeframe:int, money_amount:float, 
        stoploss:float, stopgain: float, martingales=0, factor=1.0, soros=0
    ) -> None:
        self.asset          = asset
        self.timeframe      = timeframe
        self.money_amount   = money_amount
        self.stoploss       = stoploss
        self.stopgain       = stopgain
        self.martingales    = martingales
        self.factor         = factor
        self.soros          = soros