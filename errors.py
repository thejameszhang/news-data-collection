class TickersError(Exception):
    def __init__(self, message="Specify either tickers or num_tickers."):
        self.message = message
        super().__init__(self.message)