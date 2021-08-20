from src.Bollinger.Bollinger_trader import BollingerTrader
from src.SMA.SMA_trader import SMATrader

class Trading_Strategies():
    def __init__(self, strategy: str):
        self.strategy = strategy

    def bollinger_strategy(self):
        bollinger_trader = BollingerTrader(
            "/Users/romain/trading-bot/oanda.cfg",
            "EUR_USD",
            "1min",
            SMA=50,
            dev=2,
            units=100000
        )
        bollinger_trader.get_most_recent()
        bollinger_trader.stream_data(bollinger_trader.instrument, stop=100)
        if bollinger_trader.position != 0:
            close_order = bollinger_trader.create_order(
                bollinger_trader.instrument,
                units=-bollinger_trader.position * bollinger_trader.units,
                suppress=True,
                ret=True
            )
            bollinger_trader.report_trade(close_order, "GOING NEUTRAL")
            bollinger_trader.position = 0

    def sma_strategy(self):
        sma_trader = SMATrader(
            "/Users/romain/trading-bot/oanda.cfg",
            "EUR_USD",
            "1min",
            SMA_short=50,
            SMA_long=200,
            units=100000
        )
        sma_trader.get_most_recent()
        sma_trader.stream_data(sma_trader.instrument, stop=30)
        if sma_trader.position != 0:
            close_order = sma_trader.create_order(
                sma_trader.instrument,
                units=-sma_trader.position * sma_trader.units,
                suppress=True,
                ret=True
            )
            sma_trader.report_trade(close_order, "GOING NEUTRAL")
            sma_trader.position = 0

    def launch_trading_strategy(self):
        if self.strategy == 'bollinger':
            self.bollinger_strategy()
        elif self.strategy == 'sma':
            self.sma_strategy()

test = Trading_Strategies('bollinger')
test.launch_trading_strategy()