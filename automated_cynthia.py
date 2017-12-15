from scrapers.ratecity import RateCity
from pprint import pprint
import sys


def main(argv):
    ratecity = RateCity()
    # pprint(ratecity.lenders())
    ratecity.to_csv(ratecity.products(), 'ratecity.csv')
    # pprint(ratecity.products())

if __name__ == "__main__":
    main(sys.argv)
