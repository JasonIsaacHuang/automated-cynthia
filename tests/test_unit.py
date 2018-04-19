import pytest

from scrapers.Finder import Finder
from models.Product import Product


def test_to_dict():
	product_url = 'https://www.finder.com.au/adelaide-bank-smartsaver-home-loan#22835'
	finder = Finder()
	product = Product(finder, product_url, None)
	# pprint.pprint(product.to_dict())