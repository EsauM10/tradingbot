# TradingBot
Bot IQ Option escalável onde é possível criar e testar diferentes estratégias de análise técnica e probabilística.

OBS: As estratégias implementadas aqui são apenas para propósitos de estudo, use sua conta no modo treinamento

## Dependências
 - python (3.7+)
 - numpy
 - [iqoptionapi](https://github.com/iqoptionapi/iqoptionapi)

## Instalar
`pip install git+https://github.com/EsauM10/tradingbot.git`

## Como Iniciar
OBS: O bot é programado para parar toda vez que os valores de stopgain/stoploss são atingidos
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
from trading import Action
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
