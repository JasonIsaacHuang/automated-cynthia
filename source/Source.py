import json
from .Lender import Lender
from scrapers.Finder import Finder
from scrapers.Mozo import Mozo
from scrapers.RateCity import RateCity

class Source:

    # Construct with different source configurations
    def __init__(self, *sources):

        self._source_config = json.load(open('source/source_config.json'))
        # Collection of valid sources
        self._sources = {}

        sources = [src.lower() for src in sources]
        for src in sources:
            if src in self._source_config['source']:
                scraper = None
                if src == 'finder':
                    scraper = Finder()
                elif src == 'ratecity':
                    scraper = RateCity()
                elif src == 'mozo':
                    scraper = Mozo()
                self._sources[src] = scraper

        self._lender_config = json.load(open('source/lender_config.json'))
        # Collection of lenders available from the given sources
        self._lenders = {}

        for src in self._sources.values():
            pass



    def sources(self):
        return list(self._sources.keys())

    def url_of(self, source):
        if source in self._sources.keys() and source in self._source_config.keys():
            return self._source_config[source]

    def lender(self, lender):
        return Lender(self, lender)