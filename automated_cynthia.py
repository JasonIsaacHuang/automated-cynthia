from scrapers.ratecity import RateCity
from scrapers.finder import Finder
from utils import Log
import argparse
import sys


def main(argv):
    parser = argparse.ArgumentParser(description='Scrapes various websites for mortgages')
    parser.add_argument('-s', '--source', help='choose which sources to scrape from', nargs='+')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-q', '--quiet', action='store_true')
    group.add_argument('-v', '--verbose', action='store_true')
    group.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()
    log = Log()

    if args.quiet:
        log.i('silent output enabled')
        log.verbosity = -1
    if args.verbose:
        log.i('verbose output enabled')
        log.verbosity = 1
    if args.debug:
        log.i('debug output enabled')
        log.verbosity = 2

    if args.source:
        for source in set(args.source):
            if source.lower() == 'ratecity':
                log.i('Scraping from RateCity')
                ratecity = RateCity(log)
                ratecity.to_csv(ratecity.products(), 'ratecity.csv')
            elif source.lower() == 'finder':
                log.i('Scraping from Finder')
                finder = Finder(log)
                finder.to_csv(finder.products(), 'finder.csv')
            else:
                log.i(source + ' not a valid source, skipping...')
    else:
        log.i("no source specified, scraping from all sources")


if __name__ == "__main__":
    main(sys.argv)
