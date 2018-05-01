from scrapers.Scraper import Scraper


class MockScraper(Scraper):

	def __init__(self):
		self._name = 'Mock Scraper'

	def name(self):
		return self._name

	def lenders(self):
		pass

	def products(self, lender_url):
		pass

	def product_information(self, product_url):
		pass