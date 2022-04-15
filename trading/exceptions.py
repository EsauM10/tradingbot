class StopLossReached(Exception):
    pass

class StopGainReached(Exception):
    pass

class StopTradingBot(Exception):
    pass

class TransactionCanceled(Exception):
    pass

class HoldAction(Exception):
    pass