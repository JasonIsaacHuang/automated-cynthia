from abc import ABC, abstractmethod, abstractproperty

class Scraper(ABC):
	
	@abstractproperty
	def base_url(self):
		pass

	@abstractmethod
	def lenders(self):
		pass
	
	@abstractmethod
	def products(self):
		pass
	
	@abstractmethod
	def product(self):
		pass
	
