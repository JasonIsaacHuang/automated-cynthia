from bs4 import BeautifulSoup
from .Scraper import Scraper
from utils import invert_dict
from source.Lender import Lender
import json
import requests


class RateCity(Scraper):

    def __init__(self):
        self._name = 'RateCity'
        self.base_url = 'http://www.ratecity.com.au'

    def name(self):
        return self._name

    """
    Returns all the lenders that are available from Finder

    Returns:
        A dictionary of lenders to urls available from Finder
    """
    def lenders(self):
        url = self.base_url + '/home-loans/companies'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        accepted_lenders = invert_dict(json.load(open('config.json'))['lenders'])

        lender_dict = {}

        for lender in soup.find_all('div', class_='company-item'):
            lender_name = lender.parent.parent.attrs['href']
            if lender_name in accepted_lenders.keys():
                standardised_lender_name = accepted_lenders[lender_name]
                lender_dict[standardised_lender_name] = Lender(self, standardised_lender_name, self.base_url + '/home-loans/' + lender_name)

        return lender_dict

    """
    Returns all the products offered by the given lender

    Args:
        lender_url: Url of the lender which contains product links

    Returns:
        A dictionary of products to urls of the offered products
    """
    def products(self, lender_url):
        pass

    def product_information(self, product_url):
        pass