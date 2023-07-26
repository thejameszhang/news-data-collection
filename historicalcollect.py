from pygooglenews import GoogleNews
import yfinance as yf
import datetime as dt
from typing import List, Dict, Optional
from errors import *
import json
from abstractcollect import AbstractCollector

class HistoricalCollector(AbstractCollector):

    def collect(self):
        """
        
        """
        gn = GoogleNews(lang="en", country="en")
        date = self.start

        while (date != self.end):
            before = (date + dt.timedelta(days=1)).strftime("%Y-%m-%d")
            after = date.strftime("%Y-%m-%d")
            query = f"intitle:AAPL OR intitle:Apple after:{after} before:{before}"
            print(query)
            search = gn.search(query=query)
            entries = search["entries"]
            print(after, len(entries))
            for entry in entries:
                print(entry["title"])
            print()
            date += dt.timedelta(days=1)
        pass