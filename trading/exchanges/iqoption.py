from datetime import datetime
from typing import Literal
from trading.util import Action, Candle, Transaction
from trading.exceptions import TransactionCanceled
from trading.exchanges import Exchange
from iqoptionapi.stable_api import IQ_Option

AccountModes = Literal['REAL', 'PRACTICE']

class IQOptionExchange(Exchange):
    def __init__(self, email: str, password: str) -> None:
        self.api = IQ_Option(email, password)


    def balance(self) -> float:
        return self.api.get_balance()

    def change_account(self, mode: AccountModes):
        self.api.change_balance(mode)

    def connect(self) -> bool:
        status, reason = self.api.connect()
        if(not status): raise Exception(f'{reason}')
        return True

    def buy(self, asset:str, expiration:int, amount:float, action: Action) -> Transaction:
        direction  = 'call' if(action == Action.BUY) else 'put'
        status, id = self.api.buy(amount, asset, direction, expiration)

        if(not status): 
            raise TransactionCanceled('** Ativo/Timeframe nao disponivel\n')
        
        return Transaction(
            id=id,
            asset=asset, 
            expiration_time=expiration, 
            money_amount=amount, 
            action=action)
    

    def get_candles(self, asset:str, timeframe:int, candles_amount:int, timestamp:float) -> list[Candle]:
        if(candles_amount <= 0): return []
        if(candles_amount > 1000): 
            raise Exception('O numero maximo de candles permitidos e 1000')

        data = self.api.get_candles(asset, timeframe*60, candles_amount, timestamp)
        return [self.__format_candle(candle) for candle in data]


    def wait(self, transaction: Transaction) -> Transaction:
        result, profit = self.api.check_win_v4(transaction.id)
        transaction.status = result
        transaction.profit = round(float(profit), 2)
        return transaction

    
    def __format_candle(self, candle: dict) -> Candle:
        return Candle(
            id     = candle['id'],
            open   = candle['open'],
            close  = candle['close'],
            high   = candle['max'],
            low    = candle['min'],
            volume = candle['volume'],
            start_time = datetime.fromtimestamp(candle['from']),
            end_time   = datetime.fromtimestamp(candle['to'])
        ) 