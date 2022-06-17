import time, re
from datetime import datetime
from trading.util import Action, Candle
from trading.exceptions import StopTradingBot, TransactionCanceled
from trading.setup import TradingSetup
from trading.strategies import TradingStrategy

DATE_FORMAT = '%d/%m/%Y %H:%M'
PATTERN = r'^([0-2][0-9]|(3)[0-1])/(((0)[0-9])|((1)[0-2]));(?:[01]\d|2[0123]):(?:[012345]\d);[A-Z]{6}(-OTC){0,1};(M1|M5|M15);(CALL|PUT)$'

class Entry:
    asset: str
    timeframe: int
    action: Action
    target_hour: datetime

    def __init__(self, entry_string: str) -> None:
        self.__parse(entry_string)


    def __parse(self, entry: str):
        data = entry.split(';')
        date, hour, asset, timeframe, action = data
        date_string = f'{date}/{datetime.now().year} {hour}'

        self.asset       = asset
        self.timeframe   = int(timeframe.replace('M', ''))
        self.action      = Action.BUY if(action=='CALL') else Action.SELL
        self.target_hour = datetime.strptime(date_string, DATE_FORMAT)
    
    @property
    def hour(self) -> str:
        return self.target_hour.strftime(DATE_FORMAT)
    
    @property
    def remaining_time_in_seconds(self) -> float:
        return self.target_hour.timestamp() - time.time()

    def __eq__(self, other: object) -> bool:
        if(not isinstance(other, Entry)):       return False
        if(self.asset != other.asset):          return False
        if(self.timeframe != other.timeframe):  return False
        if(self.action != other.action):        return False
        if(self.hour != other.hour):            return False
        return True 



class ListOfSignalsStrategy(TradingStrategy):
    def __init__(self, entries: list[str], setup: TradingSetup) -> None:
        super().__init__(candles_amount=0)
        
        self.entries = self.parse_data(entries)
        self.setup   = setup

    def matches(self, entry: str) -> bool:
        if(re.match(pattern=PATTERN, string=entry)):
            return True
        return False
    
    def parse_data(self, entries: list[str]) -> list[Entry]:
        entries.reverse()
        return [Entry(entry_string=entry) for entry in entries if(self.matches(entry))]

    def evaluate(self, candles: list[Candle]) -> Action:
        if(not self.entries): raise StopTradingBot()

        entry                = self.entries.pop()
        self.setup.asset     = entry.asset
        self.setup.timeframe = entry.timeframe
        
        if(entry.remaining_time_in_seconds < 0):
            raise TransactionCanceled(f'** [{entry.asset}]: Nao foi possivel realizar a operacao')

        print(f'** [{entry.asset}]: Operacao agendada para {entry.hour}')
        time.sleep(entry.remaining_time_in_seconds)
        return entry.action
