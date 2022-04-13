class TradingSetup:
    def __init__(self, asset:str, timeframe:int, money_amount:float, 
        stoploss:float, stopgain: float, same_candle=False,
    ) -> None:
        self.asset        = asset
        self.timeframe    = timeframe
        self.same_candle  = same_candle
        self.money_amount = money_amount
        self.stoploss     = stoploss
        self.stopgain     = stopgain
