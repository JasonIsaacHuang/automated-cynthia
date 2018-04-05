import argparse
from requests import ConnectionError
import sys
import re

from models.Source import Source
from utils import Log
#
#
# def scrape_finder(log, lender_mode=False):
#     log.i('Scraping from Finder')
#     finder = Finder(log)
#     if lender_mode:
#         log.i(finder.lenders())
#     else:
#         finder.to_csv(finder.products(), 'finder.csv')
#
#
# def scrape_mozo(log, lender_mode=False):
#     log.i('Scraping from Mozo')
#     mozo = Mozo(log)
#     if lender_mode:
#         log.i(mozo.lenders())
#     else:
#         mozo.to_csv(mozo.products(), 'mozo.csv')
#
#
# def scrape_ratecity(log, lender_mode=False):
#     log.i('Scraping from RateCity')
#     ratecity = RateCity(log)
#     if lender_mode:
#         log.i(ratecity.lenders())
#     else:
#         ratecity.to_csv(ratecity.products(), 'ratecity.csv')
#
#
# def main(argv):
#     parser = argparse.ArgumentParser(description='Scrapes various websites for mortgages')
#     parser.add_argument('-s', '--models', help='choose which sources to scrape from [finder | ratecity]', nargs='+')
#     parser.add_argument('-l', '--lender', help='output the lenders available instead of scraping', action='store_true')
#
#     group = parser.add_mutually_exclusive_group()
#     group.add_argument('-q', '--quiet', action='store_true')
#     group.add_argument('-v', '--verbose', action='store_true')
#     group.add_argument('-d', '--debug', action='store_true')
#     args = parser.parse_args()
#     log = Log()
#
#     if args.quiet:
#         log.i('silent output enabled')
#         log.verbosity = -1
#     if args.verbose:
#         log.i('verbose output enabled')
#         log.verbosity = 1
#     if args.debug:
#         log.i('debug output enabled')
#         log.verbosity = 2
#
#     lender_mode = False
#     if args.lender:
#         lender_mode = True
#
#     if args.models:
#         for models in set(args.models):
#             if models.lower() == 'finder':
#                 scrape_finder(log, lender_mode)
#             elif models.lower() == 'mozo':
#                 scrape_mozo(log, lender_mode)
#             elif models.lower() == 'ratecity':
#                 scrape_ratecity(log, lender_mode)
#             else:
#                 log.i(models + ' not a valid models, skipping...')
#     else:
#         log.i("no models specified, scraping from all sources")
#         scrape_finder(log, lender_mode)
#         scrape_mozo(log, lender_mode)
#         scrape_ratecity(log, lender_mode)

def main(argv):
    parser = argparse.ArgumentParser(description='Collects mortgage product data from various websites')
    parser.add_argument('-s', '--models', help='choose which sources to scrape from [finder | ratecity | mozo]', nargs='+')
    # parser.add_argument('-l', '--lender', help='output the lenders available instead of scraping', action='store_true')

    args = parser.parse_args()

    log = Log()
    log.verbosity = 1

    sources = None
    if args.source:
        sources = args.source

    try:
        source_object = Source(log, ['finder', ''])

        log.i("Configured with " + str(source_object.sources()))

        log.i("Finding all lenders\n")

        all_lenders = source_object.all_lenders()

        for lender in all_lenders:
            products = lender.products()
            for product in products.values():
                if product.is_valid():
                    print(product.url())
                    print(product.name())

    except ConnectionError:
        print("There is something wrong with the internet connection.")


if __name__ == "__main__":
    main(sys.argv)