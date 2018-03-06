from abc import ABC, abstractmethod

class Scraper(ABC):

    def __str__(self):
        return self.name()

    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def lenders(self):
        pass

    @abstractmethod
    def products(self, lender_url):
        pass

    @abstractmethod
    def product_information(self, product_url):
        pass