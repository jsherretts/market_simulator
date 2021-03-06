import pandas as pd

from market_trading.markets.MarketBase import MarketBase


class BTCMarketSimulator(MarketBase):
    "return price for every minute"
    def __init__(self, start_timestamp, btc_price_csv, end_timestamp=None):
        super().__init__(start_timestamp)
        btc_df  = pd.read_csv(btc_price_csv)

        self.btc_df= (
            btc_df[(btc_df['Timestamp'] >= start_timestamp) &
                   (btc_df['Timestamp'] < end_timestamp if end_timestamp else True)]
            .interpolate(axis=0)
            .sort_values('Timestamp', ascending=True)
            .reset_index().drop(columns=['index'])
        )

        self.crnt_time = 0

    def get_current_price(self):
        """
        the price for next minute
        Returns:

        """
        crnt_row = self.btc_df.iloc[self.crnt_time]
        return {
            'open': crnt_row.Open,
            'close': crnt_row.Close,
            'high': crnt_row.High,
            'low': crnt_row.Low
        }

    def get_current_timestamp(self):
        return self.btc_df.iloc[self.crnt_time].Timestamp

    def __iter__(self):
        self.crnt_time = 0
        return self

    def __next__(self):
        if self.crnt_time >= len(self.btc_df):
            raise StopIteration
        price_candle = self.get_current_price()
        ts = self.get_current_timestamp()
        self.crnt_time += 1
        return ts, price_candle


    def get_percentage_done(self):
        return int(100 * (self.crnt_time) / len(self.btc_df))

    def get_closing_price(self):
        return self.btc_df.iloc[-1].Close

    def get_opening_price(self):
        return self.btc_df.iloc[0].Close
