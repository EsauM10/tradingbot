import time, re
from datetime import datetime
from trading import Action, Candle
from trading.exceptions import StopTradingBot
from trading.setup import TradingSetup
from trading.strategies import TradingStrategy

DATE_FORMAT = '%d/%m/%Y %H:%M'
PATTERN = '^([0-2][0-9]|(3)[0-1])/(((0)[0-9])|((1)[0-2]));(?:[01]\d|2[0123]):(?:[012345]\d);[A-Z]{6}(-OTC){0,1};(M1|M5|M15);(CALL|PUT)$'

class Entry:    
    def __init__(self, asset:str, timeframe:str, action:str, date_string:str) -> None:
        self.asset       = asset
        self.timeframe   = int(timeframe.replace('M', ''))
        self.action      = Action.BUY if(action=='CALL') else Action.SELL
        self.target_hour = self.parse_string_to_datetime(date_string)

    def parse_string_to_datetime(self, date_string:str) -> datetime:
        return datetime.strptime(date_string, DATE_FORMAT)
    
    @property
    def hour(self) -> str:
        return self.target_hour.strftime(DATE_FORMAT)
    


class ListOfSignalsStrategy(TradingStrategy):
    def __init__(self, entries: list[str], setup: TradingSetup) -> None:
        super().__init__(candles_amount=0)
        
        self.entries = self.parse_data(entries)
        self.setup   = setup

    def parse_data(self, entries: list[str]) -> list[Entry]:
        entries.reverse()
        return [self.parse_entry(entry) for entry in entries if(self.matchs(entry))]

    def parse_entry(self, entry:str) -> Entry:
        '''Transforma uma string no formato ex: 01/02;00:00;EURUSD;M1;PUT'''
        data = entry.split(';')
        date, hour, asset, timeframe, action = data
        date_string = f'{date}/{datetime.now().year} {hour}'
        return Entry(asset=asset, timeframe=timeframe, action=action, date_string=date_string)
    
    def matchs(self, entry: str):
        return re.match(pattern=PATTERN, string=entry)

    def evaluate(self, candles: list[Candle]) -> Action:
        if(not self.entries): raise StopTradingBot()

        entry = self.entries.pop()
        self.setup.asset     = entry.asset 
        self.setup.timeframe = entry.timeframe
        action      = entry.action
        sleep_time  = entry.target_hour.timestamp() - time.time() 
        
        if(sleep_time < 0): 
            print(f'** [{entry.asset}]: Não foi possivel realizar a operacao')
            return Action.HOLD

        print(f'** [{entry.asset}]: Operacao agendada para {entry.hour}')
        time.sleep(sleep_time)
        return action
