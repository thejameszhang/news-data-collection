from abc import ABC, abstractmethod
from errors import TickersError
import json
import yfinance as yf
import datetime as dt
from typing import Dict, List, Optional
import sys
sys.path.append("../")
from sif.sifinfra.sif_utils import get_universe_tickers

class AbstractCollector(ABC):
    def __init__(self, start: dt.datetime, 
                 end: dt.datetime, 
                 tickers: Optional[List[int]] = None,
                 num_tickers: Optional[int] = 0, 
                 dump: Optional[bool] = False):
        self.start = start
        self.end = end
        self.tickers = tickers
        self.num_tickers = num_tickers
        if not self.tickers and not self.num_tickers:
            raise TickersError()
        if self.num_tickers:
            self.tickers = get_universe_tickers(num_tickers, start, end)
            if self.dump:
                with open("tickers.json", "w") as fp:
                    json.dump(tickers, fp)
        self.assets = self.get_assets(self.tickers)
            
    def get_assets(self, tickers: List[str]) -> Dict[str, str]:
        """
        Search queries return the most accurate information reflecting company
        sentiment when they contain the company name, not the ticker.
        :param: list of tickers
        :return: dictionary of tickers to names
        """
        # Retrieves a list of yfinance objects.
        fillers = ("Inc", "Incorporated", "Corp", "Corporation", "Holding", 
                "Holdings", "Co", "Limited", "Ltd", "Company", "Group", "The")
        try:
            with open("assets.json", "r") as fp:
                assets = json.load(fp)
            assets = {ticker : assets[ticker] for ticker in tickers if ticker in assets.keys()}
        except: 
            assets = {}
            yftickers = list(yf.Tickers(tickers).tickers.values())
            for ticker in yftickers:
                try:
                    name = ticker.info["longName"]
                    name = name.replace(",", "").replace(".", "")
                    assets[ticker.ticker] = name
                except:
                    pass
            assets = self.remove_fillers(assets)
            if self.dump:
                with open("assets.json", "w") as fp:
                    json.dump(assets, fp)
        return assets

    def remove_fillers(self, assets: Dict[str, str]) -> Dict[str, str]:
        """
        
        """
        # Remove words such as "Inc" and "Corp".
        fillers = ("inc", "incorporated", "corp", "corporation", "holding", 
                "holdings", "co", "limited", "ltd", "company", "group", "the", 
                "plc", "companies")
        for ticker in assets:
            name = assets[ticker].split(" ")
            name = [n.lower() for n in name if n.lower() not in fillers]
            name = " ".join(name)
            assets[ticker] = name
        return assets

    @abstractmethod
    def collect(self):
        pass