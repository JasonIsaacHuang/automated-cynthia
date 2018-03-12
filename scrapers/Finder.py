from bs4 import BeautifulSoup
from .Scraper import Scraper
from utils import invert_dict
from source.Lender import Lender
from source.Product import Product
import json
import re
import requests


class Finder(Scraper):

    def __init__(self):
        self._name = 'Finder'
        self.base_url = 'https://www.finder.com.au'
        # list of dud pages to ignore
        self.dud_pages = [
            'https://www.finder.com.au/home-loans-enquiry-page',
            'https://www.finder.com.au/home-loans/aussie-mortgage-broker-enquiry',
            'https://www.finder.com.au/home-loans/choice-home-loans-enquiry'
        ]

    def name(self):
        return self._name

    """
    Returns all the lenders that are available from Finder.

    Returns:
        A dictionary of lender names to lender instances available from Finder.
    """
    def lenders(self):

        url = self.base_url + '/home-loans/view-more-home-loans'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        accepted_lenders = invert_dict(json.load(open('config.json'))['lenders'])

        lender_dict = {}

        for lender in soup.find(class_='az-listing js-az-listing').find(class_='hide-desktop').find_all('li', class_='az-listing__item'):
            if '/home-loans/' in lender.find('a').attrs['href']:
                lender_name = lender.find('a').text.strip()
                lender_url = lender.find('a').attrs['href']

                if lender_name in accepted_lenders.keys():
                    standardised_lender_name = accepted_lenders[lender_name]
                    lender_dict[standardised_lender_name] = Lender(self, standardised_lender_name, lender_url)
        return lender_dict

    """
    Returns all the products offered by the given lender.
    Some of the product urls contains multiple variants inside.
    We need to also capture each of those variants as a separate product instance.
    
    Args:
        lender_url: Url of the lender which contains product links.
    
    Returns:
        A dictionary of product names to product instances of the offered products.
    """
    def products(self, lender_url):

        response = requests.get(lender_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        product_group_dict = {}

        # three scenarios found:
        # has product range
        # no product range, has only products
        # no product range or products - skip

        # find all product ranges
        for product in soup.find_all('a', class_='enquire-link-arrow'):
            # check that it is not a dud page
            # check that the url does not direct outside of the source
            if product not in self.dud_pages and self.valid_url(product):
                product_name = product.parent.find('h4').text
                product_url = product.attrs['href']
                # before inserting, check if this url is already captured
                if product_url not in product_group_dict.values():
                    product_group_dict[product_name] = product_url

        # some products don't have a range so it needs to be inferred from the product listing
        if soup.find('table', class_=re.compile('comparison-table')):
            for product in soup.find('table', class_=re.compile('comparison-table')).find_all('td', class_='comparison-table__name'):
                # strip out the query string from the url
                product_name = product.find('a').text.split(' - ')[0]
                product_url = product.find('a').attrs['href'].split('?')[0]
                # check that it is not a dud page
                # check that the url does not direct outside of the source
                # check if this url is not already captured
                if (product_url not in self.dud_pages and self.valid_url(product_url) and product_url not in product_group_dict.values()):
                    product_group_dict[product_name] = product_url

        # At this point, we have a list of product_urls which may or may not have multiple variants inside.
        # Need to go to each page and determine how many variants there are and create a product instance for each.
        product_variant_dict = {}

        for product_name, product_url in product_group_dict.items():
            product_variant_dict.update(self.product_variant(product_name, product_url))

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

        # not all products have variants
        if soup.find('div', class_=re.compile('productVariantTable')):
            for variant in soup.find('div', class_=re.compile('productVariantTable')).find('tbody').find_all('tr'):
                variant_url = product_url + '#' + variant.attrs['data-product-id']
                if self.valid_url(variant_url):
                    variant_name = variant.find('td').text
                    product_variant_dict[product_name + ' ' + variant_name] = Product(self, variant_url, product_name)

        # create self as an product instance
        else:
            product_variant_dict[product_name] = Product(self, product_url)

        return product_variant_dict

    """
    Returns all information available for a given product.
    The information is stored in a dictionary where the keys are defined in the config for standardisation.
    
    Args:
        product_url: Url to the product.
        
    Return:
        A dictionary containing all of the product information.
    """
    def product_information(self, product_url):

        response = requests.get(product_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        product_information = {}

        try:
            details = soup.find('div', class_=re.compile('defaultInfobox'))

            try:
                product_information['Url'] = product_url
            except Exception:
                pass

            try:
                product_information['Name'] = details.find('table').find('tr').find('th', text='Product Name').parent.find('td').text
            except Exception:
                pass

            try:
                product_information['Rate Type'] = details.find('table').find('th', text='Interest Rate Type').parent.find('td').text
            except Exception:
                pass

            try:
                product_information['Min Loan Amount'] = details.find('table').find('th', text='Minimum Loan Amount').parent.find('td').text
            except Exception:
                pass

            try:
                product_information['Max Loan Amount'] = details.find('table').find('th', text='Maximum Loan Amount').parent.find('td').text
            except Exception:
                pass

            try:
                product_information['Min Loan Term'] = details.find('table').find('th', text='Minimum Loan Term').parent.find('td').text
            except Exception:
                pass

            try:
                product_information['Max Loan Term'] = details.find('table').find('th', text='Maximum Loan Term').parent.find('td').text
            except Exception:
                pass

            try:
                product_information['Mortgage Offset Account'] = details.find('table').find('th', text='Mortgage Offset Account').parent.find('td').text
            except Exception:
                pass

            try:
                product_information['Loan Redraw Facility'] = details.find('table').find('th', text='Loan Redraw Facility').parent.find('td').text
            except Exception:
                pass

            try:
                product_information['Split Loan Facility'] = details.find('table').find('th', text='Split Loan Facility').parent.find('td').text
            except Exception:
                pass

            try:
                product_information['Fixed Interest Option'] = details.find('table').find('th', text='Fixed Interest Option').parent.find('td').text
            except Exception:
                pass

            try:
                product_information['Suitable for Investment'] = details.find('table').find('th', text='Suitable for Investment').parent.find('td').text
            except Exception:
                pass

            try:
                product_information['Extra Repayment'] = details.find('table').find('th', text='Extra Repayment').parent.find('td').text
            except Exception:
                pass

            try:
                product_information['Available as equity loan/line of credit'] = details.find('table').find('th', text='Available as equity loan/line of credit').parent.find('td').text
            except Exception:
                pass

            try:
                product_information['Repayment Type'] = details.find('table').find('th', text='Repayment Type').parent.find('td').text
            except Exception:
                pass

            # variant specific details are not properly loaded upon page load, must collect from the variant table instead
            try:
                variant_id = product_url.split('#')[1]
                try:
                    product_information['Variant'] = soup.find('div', class_=re.compile('productVariantTable')).find('tbody').find('tr', {'data-product-id': variant_id}).find('td', class_=re.compile('title')).text
                except Exception:
                    pass
                try:
                    product_information['Name'] = product_information['Name'] + ' ' + product_information['Variant']
                except Exception:
                    pass

                try:
                    product_information['Interest Rate'] = soup.find('div', class_=re.compile('productVariantTable')).find('tbody').find('tr', {'data-product-id':variant_id}).find('td', class_=re.compile('interest-rate')).find('span').text
                except Exception:
                    pass

                try:
                    product_information['Comparison Rate'] = soup.find('div', class_=re.compile('productVariantTable')).find('tbody').find('tr', {'data-product-id':variant_id}).find('td', class_=re.compile('interest-rate')).find('div', class_='variant-comp-rate').find('span').text
                except Exception:
                    pass

                max_insured_lvr_index = soup.find('div', class_=re.compile('productVariantTable')).find('thead').find('tr').index(soup.find('div', class_=re.compile('productVariantTable')).find('thead').find('tr').find('th', text=re.compile('Max Insured LVR')))
                try:
                    product_information['Max Insured LVR'] = soup.find('div', class_=re.compile('productVariantTable')).find('tbody').find('tr', {'data-product-id':variant_id}).find_all('td')[max_insured_lvr_index].text
                except Exception:
                    pass

                max_insured_lvr_index = soup.find('div', class_=re.compile('productVariantTable')).find('thead').find('tr').index(soup.find('div', class_=re.compile('productVariantTable')).find('thead').find('tr').find('th', text=re.compile('Max LVR')))
                try:
                    product_information['Max LVR'] = soup.find('div', class_=re.compile('productVariantTable')).find('tbody').find('tr', {'data-product-id':variant_id}).find_all('td')[max_insured_lvr_index].text
                except Exception:
                    pass
            except Exception:
                pass
        except Exception:
            pass

        return product_information

    def valid_url(self, url):
        return self.base_url in url