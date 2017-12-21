from scrapers.ratecity import RateCity
from scrapers.finder import Finder
import argparse
import sys


def main(argv):
    parser = argparse.ArgumentParser(description='Scrapes various websites for mortgages')
    parser.add_argument('-q', '--quiet', help='suppress all output', action='store_true')
    parser.add_argument('-s', '--source', help='choose which sources to scrape from', nargs='+')
    args = parser.parse_args()

    if args.quiet:
        print('suppressing all output')
        print('TODO')
    if args.source:
        for source in set(args.source):
            if source.lower() == 'ratecity':
                print('Scraping from RateCity')
                ratecity = RateCity()
                ratecity.to_csv(ratecity.products(), 'ratecity.csv')
            elif source.lower() == 'finder':
                print('Scraping from Finder')
                finder = Finder()
                finder.to_csv(finder.products(), 'finder.csv')
            else:
                print(source + ' not a valid source, skipping...')

    else:
        print("no source specified, scraping from all sources")


if __name__ == "__main__":
    main(sys.argv)
