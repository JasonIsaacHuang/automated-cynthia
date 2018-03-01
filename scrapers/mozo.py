from bs4 import BeautifulSoup
from utils import invert_dict
from .model import Scraper
import json
import re
import requests


class Mozo(Scraper):

    base_url = 'https://mozo.com.au'

    def _lenders(self):
        url = self.base_url + '/home-loans/resources/providers'
        response = requests.get(url)
        souped_response = BeautifulSoup(response.content, "html.parser")

        lender_list = []

        accepted_lenders = invert_dict(json.load(open('config.json'))['lenders'])

        base = souped_response.find(text='Home loan providers')

        for lender_alpha in base.parent.parent.find_all('div'):
            for lender in lender_alpha.find_all('div'):
                lender_name = lender.find('a').text.strip()
                lender_url = lender.find('a').attrs['href']

                if lender_name in accepted_lenders.keys():
                    lender_tuple = (accepted_lenders[lender_name], lender_url)
                    lender_list.append(lender_tuple)
                    self.log.v(lender_name)
                else:
                    self.log.v('skip - ' + lender_name)
        try:
            pass
        except Exception:
            raise Exception('Parsing error in' + url)

        return lender_list

    def _products(self):
        
        product_list = []

        # fetch all lenders
        lenders = self.lender_list
        if lenders == [] or lenders is None:
            lenders = self._lenders()

        num_lenders = len(lenders)
        # visit each lender as this will contain all the products available
        for idx, (_, url) in enumerate(lenders):
            lender_progress = '[' + str(idx + 1).zfill(len(str(num_lenders))) + '/' + str(num_lenders) + ']'
            print(url)
