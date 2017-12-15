from bs4 import BeautifulSoup
from .model import Scraper
import csv
import re
import requests

class RateCity(Scraper):

    base_url = 'http://www.ratecity.com.au'

    def _lenders(self):
        url = self.base_url + '/home-loans/companies'
        response = requests.get(url)
        souped_response = BeautifulSoup(response.content, "html.parser")

        lender_list = []

        try:
            for lender in souped_response.find_all('div', class_='company-item'):
                try:
                    lender_list.append(lender.parent.parent.attrs['href'])
                except Exception as e:
                    pass
        except Exception as e:
            raise Exception('Parsing error in' + url)

        return lender_list

    def _products(self):
        url = self.base_url + '/home-loans/search?h_per_page=1000'
        response = requests.get(url)
        souped_response = BeautifulSoup(response.content, "html.parser")

        products_list = []
        products_urls = []

        try:
            # Collect a list of product urls first
            result_set = souped_response.find(class_='hidden-xs-ratetable').find('tbody')

            for product in result_set.find_all('tr'):
                products_urls.append(product.find('td', class_='attribute company clickable-link').find('div').find('a').attrs['href'])

        except Exception as e:
            raise Exception('Parsing error in' + url)

        # Go to each individual page and fetch the data there
        for idx, product in enumerate(products_urls):
            print("[" + str(idx+1) + "/" + str(len(products_urls)) + "] Fetching " + product)
            product = self.product(self.base_url + product)
            products_list.append(product)

        return products_list

    def product(self, url):
        object = {}
    
        response = requests.get(url + '?h_flexibilityScore=30') # need the suffix for some pages to load properly
        souped_response = BeautifulSoup(response.content, "html.parser")
        try:
            object['Name'] = souped_response.find('h1', property='name').find('div').text
        except Exception as e:
            # Name is required or else this product would be useless
            return {}

        try:
            object['Lender'] = souped_response.find('ol', class_='breadcrumb').find('a', href=re.compile('/home-loans/.+')).find('span', property='name').text
        except Exception as e:
            # Lender is required or else this product would be useless
            return {}

        try:
            object['Advertised rate'] = souped_response.find(text='Advertised rate').parent.parent.find(class_='cell-value').text
        except Exception as e:
            object['Advertised rate'] = 'N/A'

        try:
            object['Comparison rate'] = souped_response.find(text='Comparison rate*').parent.parent.find(class_='cell-value').text
        except Exception as e:
            object['Comparison rate'] = 'N/A'

        try:
            detail_fees = souped_response.find('h4', text='Details & Fees').parent

            try:
                object['LVR'] = detail_fees.find('th', class_='maxLvr attribute').parent.find('td').find('div').find('span', class_='cell-value').text
            except Exception as e:
                object['LVR'] = 'N/A'

            try:
                object['Rate Type'] = detail_fees.find('th', class_='rateType attribute').parent.find('td').find('div').find('span', class_='cell-value').text
            except Exception as e:
                object['Rate Type'] = 'N/A'

            try:
                object['Borrowing range'] = detail_fees.find('th', class_='borrowingRange attribute').parent.find('td').find('div').find('span', class_='cell-value').text
            except Exception as e:
                object['Borrowing range'] = 'N/A'

            try:
                if detail_fees.find('th', class_='principalAndInterest attribute').parent.find('td').find('div').find('span', class_='fa fa-check'):
                    object['Principal & Interest'] = True
                elif detail_fees.find('th', class_='principalAndInterest attribute').parent.find('td').find('div').find('span', class_='fa fa-minus'):
                    object['Principal & Interest'] = False
            except Exception as e:
                pass
            
            try:
                if detail_fees.find('th', class_='interestOnly attribute').parent.find('td').find('div').find('span', class_='fa fa-check'):
                    object['Interest Only'] = True
                elif detail_fees.find('th', class_='interestOnly attribute').parent.find('td').find('div').find('span', class_='fa fa-minus'):
                    object['Interest Only'] = False
            except Exception as e:
                pass

            try:
                object['Loan Term'] = detail_fees.find('th', class_='loanTerm attribute').parent.find('td').find('div').find('span', class_='cell-value').text
            except Exception as e:
                object['Loan Term'] = 'N/A'

            try:
                if detail_fees.find('th', class_='offsetAccount attribute').parent.find('td').find('div').find('span', class_='fa fa-minus'):
                    object['Offset Account'] = "None"
                elif detail_fees.find('th', class_='offsetAccount attribute').parent.find('td').find('div').find('span', class_='fa fa-check'):
                    object['Offset Account'] = detail_fees.find('th', class_='offsetAccount attribute').parent.find('td').find('div').find('span', class_='cell-details').text
            except Exception as e:
                pass

            try:
                object['Extra Repayments'] = detail_fees.find('th', class_='extraRepayments attribute').parent.find('td').find('div').find('span', class_='cell-details').text
            except Exception as e:
                object['Extra Repayments'] = 'N/A'

            try:
                if detail_fees.find('th', class_='redrawFacility attribute').parent.find('td').find('div').find('span', class_='fa fa-minus'):
                    object['Redraw Facility'] = "None"
                elif detail_fees.find('th', class_='redrawFacility attribute').parent.find('td').find('div').find('span', class_='fa fa-check'):
                    object['Redraw Facility'] = detail_fees.find('th', class_='redrawFacility attribute').parent.find('td').find('div').find('span', class_='cell-details').text
            except Exception as e:
                pass

            try:
                if detail_fees.find('th', class_='splitLoan attribute').parent.find('td').find('div').find('span', class_='fa fa-check'):
                    object['Split Loan'] = True
                elif detail_fees.find('th', class_='splitLoan attribute').parent.find('td').find('div').find('span', class_='fa fa-minus'):
                    object['Split Loan'] = False
            except Exception as e:
                pass

            try:
                object['Loan Purpose'] = detail_fees.find('th', class_='suitableFor attribute').parent.find('td').find('div').find('span', class_='cell-value').text
            except Exception as e:
                object['Loan Purpose'] = 'N/A'

            try:
                object['States'] = detail_fees.find('th', class_='applicableStates attribute').parent.find('td').find('div').find('span', class_='cell-value').text
            except Exception as e:
                object['States'] = 'N/A'

            try:
                object['Repayment Frequency'] = detail_fees.find('th', class_='repaymentFrequencyOptions attribute').parent.find('td').find('div').find('span', class_='cell-value').text
            except Exception as e:
                object['Repayment Frequency'] = 'N/A'

        except Exception as e:
            # If it fails here, return what we have so that we at least know this product exists,
            pass

        return object
