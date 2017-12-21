from abc import ABC, abstractmethod, abstractproperty
import csv


class Scraper(ABC):

    lender_list = []
    product_list = []

    @abstractproperty
    def base_url(self):
        pass

    def lenders(self, force_fetch=False):

        print("Fetching lenders from " + self.base_url)
        if self.lender_list == [] or force_fetch:
            lender_list = self._lenders()

            if not lender_list == [] and lender_list is not None:
                self.lender_list = lender_list

        return self.lender_list

    @abstractmethod
    def _lenders(self):
        pass

    def products(self, force_fetch=False):

        print("Fetching products from " + self.base_url)
        if self.product_list == [] or force_fetch:
            product_list = self._products()

            if not product_list == [] and product_list is not None:
                self.product_list = product_list

        return self.product_list

    @abstractmethod
    def _products(self):
        pass

    def to_csv(self, products, file_name):

        # Prepare file_name
        if not file_name.endswith('.csv'):
            file_name += '.csv'

        file_handle = open(file_name, 'w')

        keys = set().union(*products)

        csv_writer = csv.DictWriter(file_handle, keys)
        print("Writing to " + file_name)
        csv_writer.writeheader()
        csv_writer.writerows(products)

        file_handle.close()

    def valid_url(self, url):
        return self.base_url in url

