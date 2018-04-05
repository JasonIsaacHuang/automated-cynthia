from bs4 import BeautifulSoup
from .Scraper import Scraper
from utils import invert_dict
from models.Lender import Lender
import json
import requests


class Mozo(Scraper):

    def __init__(self):
        self._name = 'Mozo'
        self.base_url = 'https://mozo.com.au'

    def name(self):
        return self._name

    def lenders(self):
        url = self.base_url + '/home-loans/resources/providers'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        lender_dict = {}

        accepted_lenders = invert_dict(json.load(open('config.json'))['lenders'])

        base = soup.find(text='Home loan providers')

        for lender_alpha in base.parent.parent.find_all('div'):
            for lender in lender_alpha.find_all('div'):
                lender_name = lender.find('a').text.strip()
                lender_url = lender.find('a').attrs['href']

                if lender_name in accepted_lenders.keys():
                    standardised_lender_name = accepted_lenders[lender_name]
                    lender_dict[standardised_lender_name] = Lender(self, standardised_lender_name, lender_url)

        return lender_dict

    def products(self, lender_url):
        pass

    def product_information(self, product_url):
        pass