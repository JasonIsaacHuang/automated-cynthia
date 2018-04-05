from bs4 import BeautifulSoup
from .Scraper import Scraper
from Log import invert_dict
from models.Lender import Lender
from models.Product import Product
import json
import re
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
    Returns all the products offered by the given lender.
    Some of the product urls contains multiple variants inside.
    We need to also capture each of those variants as a separate product instance.

    Args:
        lender_url: Url of the lender which contains product links

    Returns:
        A dictionary of products to urls of the offered products
    """
    def products(self, lender_url):
        
        response = requests.get(lender_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        product_group_dict = {}

        # Find all product ranges
        try:
            for product_group in soup.find('h4', class_='section-heading').parent.find_all('div', class_=re.compile('family-wrapper')):
                product_group_name = product_group.find('h4').text
                product_group_url = product_group.find('a', text='More Details').attrs['href']
                product_group_dict[product_group_name] = self.base_url + '/' + product_group_url
        except Exception:
        # Ignore if there are no product ranges
            pass
        
        product_variant_dict = {}

        # Go into each of the product ranges and collect all the individual products
        for product_group_name, product_group_url in product_group_dict.items():
            product_variant_dict.update(self.product_variant(product_group_name, product_group_url))

        # On each of the lender pages, there are a small list of products

        for product in soup.find('div', class_='rate-table-container home-loans').find('tbody').find_all('tr', class_='product'):
            product_name = product.find('td', class_=re.compile('productName')).find('div').find('a').find('span', class_='product-title').text
            product_url = self.base_url + product.find('td', class_=re.compile('productName')).find('div').find('a').attrs['href']
            product_variant_dict[product_name] = Product(self, product_url, product_name)


        return product_variant_dict


    """
    Returns all the variants offered under a given product.
    
    Args:
        product_name: Name of the base product, used to group product variants together.
        product_url: Url to the product that may potentially contain variants.
        
    Return:
        A dictionary of variant names to variant instances offered under a given product.
    """
    def product_variant(self, product_name, product_url):
        
        product_variant_dict = {}
        response = requests.get(product_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        for variant in soup.find('div', class_='rate-table-container home-loans').find('tbody').find_all('tr', class_='product'):
            variant_name = variant.find('td', class_=re.compile('productName')).find('div').find('a').find('span', class_='product-title').text
            variant_url = self.base_url + variant.find('td', class_=re.compile('productName')).find('div').find('a').attrs['href']
            product_variant_dict[variant_name] = Product(self, variant_url, product_name)

        return product_variant_dict


    def product_information(self, product_url):
        response = requests.get(product_url) # need the suffix for some pages to load properly
        souped_response = BeautifulSoup(response.content, "html.parser")

        product_information = {}

        try:
            product_information['Name'] = souped_response.find('h1', property='name').find('div').text
        except Exception as e:
            # Name is required or else this product would be useless
            return {}

        try:
            product_information['Lender'] = souped_response.find('ol', class_='breadcrumb').find('a', href=re.compile('/home-loans/.+')).find('span', property='name').text
        except Exception as e:
            # lender is required or else this product would be useless
            return {}

        try:
            product_information['Advertised rate'] = souped_response.find(text='Advertised rate').parent.parent.find(class_='cell-value').text
        except Exception as e:
            product_information['Advertised rate'] = 'N/A'

        try:
            product_information['Comparison rate'] = souped_response.find(text='Comparison rate*').parent.parent.find(class_='cell-value').text
        except Exception as e:
            product_information['Comparison rate'] = 'N/A'

        try:
            detail_fees = souped_response.find('h4', text='Details & Fees').parent

            try:
                product_information['LVR'] = detail_fees.find('th', class_='maxLvr attribute').parent.find('td').find('div').find('span', class_='cell-value').text
            except Exception as e:
                product_information['LVR'] = 'N/A'

            try:
                product_information['Rate Type'] = detail_fees.find('th', class_='rateType attribute').parent.find('td').find('div').find('span', class_='cell-value').text
            except Exception as e:
                product_information['Rate Type'] = 'N/A'

            try:
                product_information['Borrowing range'] = detail_fees.find('th', class_='borrowingRange attribute').parent.find('td').find('div').find('span', class_='cell-value').text
            except Exception as e:
                product_information['Borrowing range'] = 'N/A'

            try:
                if detail_fees.find('th', class_='principalAndInterest attribute').parent.find('td').find('div').find('span', class_='fa fa-check'):
                    product_information['Principal & Interest'] = True
                elif detail_fees.find('th', class_='principalAndInterest attribute').parent.find('td').find('div').find('span', class_='fa fa-minus'):
                    product_information['Principal & Interest'] = False
            except Exception as e:
                pass
            
            try:
                if detail_fees.find('th', class_='interestOnly attribute').parent.find('td').find('div').find('span', class_='fa fa-check'):
                    product_information['Interest Only'] = True
                elif detail_fees.find('th', class_='interestOnly attribute').parent.find('td').find('div').find('span', class_='fa fa-minus'):
                    product_information['Interest Only'] = False
            except Exception as e:
                pass

            try:
                product_information['Loan Term'] = detail_fees.find('th', class_='loanTerm attribute').parent.find('td').find('div').find('span', class_='cell-value').text
            except Exception as e:
                product_information['Loan Term'] = 'N/A'

            try:
                if detail_fees.find('th', class_='offsetAccount attribute').parent.find('td').find('div').find('span', class_='fa fa-minus'):
                    product_information['Offset Account'] = "None"
                elif detail_fees.find('th', class_='offsetAccount attribute').parent.find('td').find('div').find('span', class_='fa fa-check'):
                    product_information['Offset Account'] = detail_fees.find('th', class_='offsetAccount attribute').parent.find('td').find('div').find('span', class_='cell-details').text
            except Exception as e:
                pass

            try:
                product_information['Extra Repayments'] = detail_fees.find('th', class_='extraRepayments attribute').parent.find('td').find('div').find('span', class_='cell-details').text
            except Exception as e:
                product_information['Extra Repayments'] = 'N/A'

            try:
                if detail_fees.find('th', class_='redrawFacility attribute').parent.find('td').find('div').find('span', class_='fa fa-minus'):
                    product_information['Redraw Facility'] = "None"
                elif detail_fees.find('th', class_='redrawFacility attribute').parent.find('td').find('div').find('span', class_='fa fa-check'):
                    product_information['Redraw Facility'] = detail_fees.find('th', class_='redrawFacility attribute').parent.find('td').find('div').find('span', class_='cell-details').text
            except Exception as e:
                pass

            try:
                if detail_fees.find('th', class_='splitLoan attribute').parent.find('td').find('div').find('span', class_='fa fa-check'):
                    product_information['Split Loan'] = True
                elif detail_fees.find('th', class_='splitLoan attribute').parent.find('td').find('div').find('span', class_='fa fa-minus'):
                    product_information['Split Loan'] = False
            except Exception as e:
                pass

            try:
                product_information['Loan Purpose'] = detail_fees.find('th', class_='suitableFor attribute').parent.find('td').find('div').find('span', class_='cell-value').text
            except Exception as e:
                product_information['Loan Purpose'] = 'N/A'

            try:
                product_information['States'] = detail_fees.find('th', class_='applicableStates attribute').parent.find('td').find('div').find('span', class_='cell-value').text
            except Exception as e:
                product_information['States'] = 'N/A'

            try:
                product_information['Repayment Frequency'] = detail_fees.find('th', class_='repaymentFrequencyOptions attribute').parent.find('td').find('div').find('span', class_='cell-value').text
            except Exception as e:
                product_information['Repayment Frequency'] = 'N/A'

        except Exception as e:
            # if it fails here, return what we have so that we at least know this product exists
            pass

        return product_information