import json
from scrapers.Finder import Finder
from scrapers.Mozo import Mozo
from scrapers.RateCity import RateCity
from utils import Log

class Source:

    # Construct with different source configurations
    def __init__(self, log=None, sources=None):
        # If no log is passed, then no logs should be outputted
        # Using Log with silent mode does the same thing
        if log is None:
            self.log = Log(verbosity=-1)
        else:
            self.log = log

        # Collection of valid sources
        self._sources = {}
        self._config = json.load(open('config.json'))

        # No sources specified, default to all sources
        if sources == None:
            sources = self._config['source']

        sources = [src.lower() for src in sources]
        for src in sources:
            if src in self._config['source']:
                scraper = None
                if src == 'finder':
                    scraper = Finder()
                elif src == 'mozo':
                    scraper = Mozo()
                elif src == 'ratecity':
                    scraper = RateCity()
                self._sources[src] = scraper

        self._lenders = None

    """
    Returns all enabled sources
    
    Returns:
        A list of all enabled sources
    """
    def sources(self):
        return list(self._sources.keys())

    """
    Establishes all the lenders that are available from each source
    
    Returns:
        No return value
    """
    def _prepare_lenders(self):

        if self._lenders == None:
            self._lenders = {}
            for src in self._sources.values():
                lenders = src.lenders()
                for lender, lender_object in lenders.items():
                    if lender not in self._lenders:
                        self._lenders[lender] = [lender_object]
                    else:
                        self._lenders[lender].append(lender_object)

        return

    def lenders(self, lender):

        self._prepare_lenders()

        if lender in self._lenders.keys():
            return self._lenders[lender]
        else:
            return []

    def all_lenders(self):
        self._prepare_lenders()

        lenders = []
        for lender in self._lenders.keys():
            lenders.extend(self.lenders(lender))
        return lenders