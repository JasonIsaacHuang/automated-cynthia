from bs4 import BeautifulSoup
from .model import Scraper
import csv
import re
import requests

class RateCity(Scraper):

    base_url = 'http://www.ratecity.com.au'

    def lenders(self):
        url = self.base_url + '/home-loans/companies'
        response = requests.get(url)
        souped_response = BeautifulSoup(response.content, "html.parser")

        providers_list = []
        try:
            for lender in souped_response.find(class_='lender').find_all('a'):
                providers_list.append(lender.attrs['href'])
        except Exception as e:
            print("Could not fetch html for lender list")

        return providers_list

    def products(self):
        url = self.base_url + '/home-loans/search?h_per_page=1000'
        response = requests.get(url)
        souped_response = BeautifulSoup(response.content, "html.parser")

        products_list = []
        try:
            result_set = souped_response.find(class_='hidden-xs-ratetable').find('tbody')
            products_urls = []
            for product in result_set.find_all('tr'):
                products_urls.append(product.find('td', class_='attribute company clickable-link').find('div').find('a').attrs['href'])

            for idx, product in enumerate(products_urls):
                print("[" + str(idx+1) + "/" + str(len(products_urls)) + "] Fetching " + product)
                products_list.append(self.product(self.base_url + product))
        except Exception as e:
            print("Could not fetch html for product list")
            raise e

        return products_list

    def product(self, url):
        object = {}
        try:
            response = requests.get(url + '?h_flexibilityScore=30') # need the suffix for some pages to load properly
            souped_response = BeautifulSoup(response.content, "html.parser")
            
            object['Name'] = souped_response.find('h1', property='name').find('div').text

            object['Lender'] = souped_response.find('ol', class_='breadcrumb').find('a', href=re.compile('/home-loans/.+')).find('span', property='name').text

            object['Advertised rate'] = souped_response.find(text='Advertised rate').parent.parent.find(class_='cell-value').text

            object['Comparison rate'] = souped_response.find(text='Comparison rate*').parent.parent.find(class_='cell-value').text

            detail_fees = souped_response.find('h4', text='Details & Fees').parent

            object['LVR'] = detail_fees.find('th', class_='maxLvr attribute').parent.find('td').find('div').find('span', class_='cell-value').text

            object['Rate Type'] = detail_fees.find('th', class_='rateType attribute').parent.find('td').find('div').find('span', class_='cell-value').text

            object['Borrowing range'] = detail_fees.find('th', class_='borrowingRange attribute').parent.find('td').find('div').find('span', class_='cell-value').text

            if detail_fees.find('th', class_='principalAndInterest attribute').parent.find('td').find('div').find('span', class_='fa fa-check'):
                object['Principal & Interest'] = True
            elif detail_fees.find('th', class_='principalAndInterest attribute').parent.find('td').find('div').find('span', class_='fa fa-minus'):
                object['Principal & Interest'] = False

            if detail_fees.find('th', class_='interestOnly attribute').parent.find('td').find('div').find('span', class_='fa fa-check'):
                object['Interest Only'] = True
            elif detail_fees.find('th', class_='interestOnly attribute').parent.find('td').find('div').find('span', class_='fa fa-minus'):
                object['Interest Only'] = False

            object['Loan Term'] = detail_fees.find('th', class_='loanTerm attribute').parent.find('td').find('div').find('span', class_='cell-value').text

            if detail_fees.find('th', class_='offsetAccount attribute').parent.find('td').find('div').find('span', class_='fa fa-minus'):
                object['Offset Account'] = "None"
            elif detail_fees.find('th', class_='offsetAccount attribute').parent.find('td').find('div').find('span', class_='fa fa-check'):
                object['Offset Account'] = detail_fees.find('th', class_='offsetAccount attribute').parent.find('td').find('div').find('span', class_='cell-details').text

            object['Extra Repayments'] = detail_fees.find('th', class_='extraRepayments attribute').parent.find('td').find('div').find('span', class_='cell-details').text

            if detail_fees.find('th', class_='redrawFacility attribute').parent.find('td').find('div').find('span', class_='fa fa-minus'):
                object['Redraw Facility'] = "None"
            elif detail_fees.find('th', class_='redrawFacility attribute').parent.find('td').find('div').find('span', class_='fa fa-check'):
                object['Redraw Facility'] = detail_fees.find('th', class_='redrawFacility attribute').parent.find('td').find('div').find('span', class_='cell-details').text

            if detail_fees.find('th', class_='splitLoan attribute').parent.find('td').find('div').find('span', class_='fa fa-check'):
                object['Split Loan'] = True
            elif detail_fees.find('th', class_='splitLoan attribute').parent.find('td').find('div').find('span', class_='fa fa-minus'):
                object['Split Loan'] = False

            object['Loan Purpose'] = detail_fees.find('th', class_='suitableFor attribute').parent.find('td').find('div').find('span', class_='cell-value').text

            object['States'] = detail_fees.find('th', class_='applicableStates attribute').parent.find('td').find('div').find('span', class_='cell-value').text

            object['Repayment Frequency'] = detail_fees.find('th', class_='repaymentFrequencyOptions attribute').parent.find('td').find('div').find('span', class_='cell-value').text
        except Exception as e:
            print("Error in " + url)

        return object
