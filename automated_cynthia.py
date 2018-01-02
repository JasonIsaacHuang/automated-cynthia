from scrapers.finder import Finder
from scrapers.mozo import Mozo
from scrapers.ratecity import RateCity
from utils import Log
import argparse
import sys


def scrape_finder(log, lender_mode=False):
    log.i('Scraping from Finder')
    finder = Finder(log)
    if lender_mode:
        log.i(finder.lenders())
    else:
        finder.to_csv(finder.products(), 'finder.csv')


def scrape_mozo(log, lender_mode=False):
    log.i('Scraping from Mozo')
    mozo = Mozo(log)
    if lender_mode:
        log.i(mozo.lenders())
    else:
        mozo.to_csv(mozo.products(), 'mozo.csv')


def scrape_ratecity(log, lender_mode=False):
    log.i('Scraping from RateCity')
    ratecity = RateCity(log)
    if lender_mode:
        log.i(ratecity.lenders())
    else:
        ratecity.to_csv(ratecity.products(), 'ratecity.csv')


def main(argv):
    parser = argparse.ArgumentParser(description='Scrapes various websites for mortgages')
    parser.add_argument('-s', '--source', help='choose which sources to scrape from [finder | ratecity]', nargs='+')
    parser.add_argument('-l', '--lender', help='output the lenders available instead of scraping', action='store_true')

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

    lender_mode = False
    if args.lender:
        lender_mode = True

    if args.source:
        for source in set(args.source):
            if source.lower() == 'finder':
                scrape_finder(log, lender_mode)
            elif source.lower() == 'mozo':
                scrape_mozo(log, lender_mode)
            elif source.lower() == 'ratecity':
                scrape_ratecity(log, lender_mode)
            else:
                log.i(source + ' not a valid source, skipping...')
    else:
        log.i("no source specified, scraping from all sources")
        scrape_finder(log, lender_mode)
        scrape_mozo(log, lender_mode)
        scrape_ratecity(log, lender_mode)


if __name__ == "__main__":
    main(sys.argv)
