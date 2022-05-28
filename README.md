# TradingBot
Bot IQ Option escalável onde é possível criar e testar diferentes estratégias de análise técnica e probabilística.

OBS: As estratégias implementadas aqui são apenas para propósitos de estudo, use sua conta no modo treinamento

## Dependências
 - python (3.9+)
 - numpy
 - [iqoptionapi](https://github.com/iqoptionapi/iqoptionapi)

## Instalar
```bash
pip install git+https://github.com/EsauM10/tradingbot.git
```

## Como Iniciar
### Seu primeiro bot
Essa é a estrutura mínima que seu bot deve ter para funcionar.

A estratégia RandomStrategy se baseia no cara ou coroa para fazer entrada, foi utilizada apenas como exemplo.
```Python
from trading.bot import TradingBot
from trading.setup import TradingSetup
from trading.strategies.random import RandomStrategy
from trading.exchanges.iqoption import IQOptionExchange

# Defina seu operacional
setup = TradingSetup(
    asset='EURUSD',
    timeframe=1,
    money_amount=1.0,
    stoploss=2.0,
    stopgain=2.0,
)

strategy = RandomStrategy() # Sua estrategia
exchange = IQOptionExchange(email, password)
bot      = TradingBot(exchange, setup, strategy)

exchange.connect()
bot.run()
print(f'** Lucro obtido: R$ {bot.profit}')
```

### Lista de sinais
Sua lista de entradas precisa estar no mesmo formato do exemplo abaixo
```Python
from trading.bot import TradingBot
from trading.setup import TradingSetup
from trading.strategies.signals import ListOfSignalsStrategy
from trading.exchanges.iqoption import IQOptionExchange

# Lista de Sinais
data = [
   '15/04;18:05;NZDUSD-OTC;M1;PUT',
   '15/04;18:20;EURUSD-OTC;M5;CALL',
   '15/04;18:30;EURUSD;M15;CALL'
]

setup    = TradingSetup(asset='', timeframe=1, money_amount=1.0, stoploss=2.0, stopgain=2.0)
strategy = ListOfSignalsStrategy(entries=data, setup=setup)
exchange = IQOptionExchange(email, password)
bot      = TradingBot(exchange, setup, strategy)

exchange.connect()
bot.run()
print(f'** Lucro obtido: R$ {bot.profit}')
```

### Alerta de preços
```Python
from trading.util import Action
from trading.bot import TradingBot
from trading.setup import TradingSetup
from trading.strategies.prices import PriceAlert, PriceMonitorStrategy
from trading.exchanges.iqoption import IQOptionExchange

setup    = TradingSetup(asset='EURUSD', timeframe=1, money_amount=1.0, stoploss=2.0, stopgain=2.0)

strategy = PriceMonitorStrategy(
    alerts=[
        PriceAlert(price=1.02370, action=Action.SELL),
        PriceAlert(price=1.02320, action=Action.BUY),
    ]
)

exchange = IQOptionExchange(email, password)
bot      = TradingBot(exchange, setup, strategy)

exchange.connect()
bot.run()
print(f'** Lucro obtido: R$ {bot.profit}')
```

## Criando sua própria estratégia
Para criar uma nova estratégia, crie uma classe que herda da classe TradingStrategy e implemente o método evaluate().

A estratégia implementada abaixo utiliza a biblioteca [TA-Lib](https://github.com/mrjbq7/ta-lib), mas é possível 
utilizar qualquer biblioteca de análise técnica como [FinTA](https://github.com/peerchemist/finta).
```Python
from talib import stream
from trading.util import Action, Candle
from trading.strategies import TradingStrategy

class BollingerBandsStrategy(TradingStrategy):
    def __init__(self) -> None:
        super().__init__(candles_amount=100) #Quantidade de candles da sua estrategia

    def evaluate(self, candles: list[Candle]) -> Action:
        close_prices      = TradingStrategy.filter_data_by(candles, key='close')
        ma_100            = stream.EMA(close_prices, timeperiod=100)
        upper, mid, lower = stream.BBANDS(close_prices, timeperiod=20, nbdevup=2.5, nbdevdn=2.5, matype=0)
        price             = close_prices[-1]
        percent           = (price-lower)/(upper-lower)
        
        print(
            f'BBANDS:\t{round(percent, 3)}\n'+
            f'Upper:\t{round(upper, 5)}\n'+
            f'Lower:\t{round(lower, 5)}\n'+
            f'EMA100:\t{round(ma_100, 5)}\n',
        )

        if(percent > 1.00 and ma_100 > upper): return Action.SELL
        if(percent < 0.00 and ma_100 < lower): return Action.BUY
        return Action.HOLD
```
Depois de criar a sua estratégia, é só usar da forma convencional
```Python
...

setup    = TradingSetup(asset='EURUSD', timeframe=1, money_amount=1.0, stoploss=2.0, stopgain=2.0)
strategy = BollingerBandsStrategy()
exchange = IQOptionExchange(email, password)
bot      = TradingBot(exchange, setup, strategy)

exchange.connect()
bot.run()
print(f'** Lucro obtido: R$ {bot.profit}')
```

## Exceptions
O bot é programado para parar toda vez que os valores de stopgain/stoploss são atingidos

Use a exception StopTradingBot para forçar a parada da sua estratégia caso precise
```Python
from trading.exceptions import StopTradingBot
...

def evaluate(self, candles: list[Candle]) -> Action:
    ...
    
    if(should_stop): raise StopTradingBot()
    ...
    return Action.HOLD
```
