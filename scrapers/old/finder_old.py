from bs4 import BeautifulSoup
from Log import invert_dict
from .model import Scraper
import json
import re
import requests


class Finder(Scraper):

    base_url = 'https://www.finder.com.au'

    def lenders(self, force_fetch=False):

        self.log.i('Fetching lenders from ' + self.base_url)
        if self.lender_list == [] or force_fetch:
            lender_list = self._lenders()

            if not lender_list == [] and lender_list is not None:
                self.lender_list = lender_list

        return [lender for lender, _ in self.lender_list]

    def _lenders(self):

        url = self.base_url + '/home-loans/view-more-home-loans'
        response = requests.get(url)
        souped_response = BeautifulSoup(response.content, 'html.parser')

        accepted_lenders = invert_dict(json.load(open('config.json'))['lenders'])

        lender_list = []

        try:
            for lender in souped_response.find(class_='az-listing js-az-listing').find(class_='hide-desktop').find_all('li', class_='az-listing__item'):
                if '/home-loans/' in lender.find('a').attrs['href']:
                    lender_name = lender.find('a').text.strip()
                    lender_url = lender.find('a').attrs['href']

                    if lender_name in accepted_lenders.keys():
                        lender_tuple = (accepted_lenders[lender_name], lender_url)
                        lender_list.append(lender_tuple)
                        self.log.v(lender_name)
                    else:
                        self.log.v('skip - ' + lender_name)
        except Exception:
            raise Exception('Parsing error in ' + url)

        return lender_list

    def _products(self):

        products_list = []

        # fetch all lenders
        lenders = self.lender_list
        if lenders == [] or lenders is None:
            lenders = self._lenders()

        num_lenders = len(lenders)
        # visit each lender as this will contain all the products available
        for idx, (_, url) in enumerate(lenders):
            lender_progress = '[' + str(idx + 1).zfill(len(str(num_lenders))) + '/' + str(num_lenders) + ']'
            self.log.i(lender_progress + ' Fetching ' + url)
            response = requests.get(url)
            souped_response = BeautifulSoup(response.content, 'html.parser')

            # three scenarios found:
            # has product range
            # no product range, has only products
            # no product range or products - skip

            # list of dud pages to ignore
            dud_pages = [
                'https://www.finder.com.au/home-loans-enquiry-page',
                'https://www.finder.com.au/home-loans/choice-home-loans-enquiry'
            ]

            # find all product ranges
            urls = []
            for product_url in souped_response.find_all('a', class_='enquire-link-arrow'):
                if product_url not in dud_pages and self.valid_url(product_url):
                    urls.append(product_url.attrs['href'])

            # some products don't have a range so it needs to be inferred from the product listing
            if souped_response.find('table', class_=re.compile('comparison-table')):
                for product in souped_response.find('table', class_=re.compile('comparison-table')).find_all('td', class_='comparison-table__name'):
                    # strip out the query string from the url
                    product_url = product.find('a').attrs['href'].split('?')[0]
                    # check if it is not a dud page
                    if product_url not in dud_pages and self.valid_url(product_url):
                        urls.append(product_url)

            # combine the pages found and remove duplicates
            urls = list(set(urls))
            num_urls = len(urls)
            for idx, url in enumerate(urls):
                lender_product_progress = len(lender_progress) * ' ' + ' [' + str(idx + 1).zfill(len(str(num_urls))) + '/' + str(num_urls) + ']'
                self.log.v(lender_product_progress + ' Fetching ' + url)

                # visit each product
                products_list.extend(self.product(url, lender_product_progress))

        return products_list

    def product(self, url, progress):

        products_list = []

        response = requests.get(url)
        souped_response = BeautifulSoup(response.content, 'html.parser')

        # each product has a number of variants
        variant_urls = []
        # not all products have variants
        if souped_response.find('div', class_=re.compile('productVariantTable')):
            for variant in souped_response.find('div', class_=re.compile('productVariantTable')).find('tbody').find_all('tr'):
                variant_url = url + '#' + variant.attrs['data-product-id']
                if self.valid_url(variant_url):
                    variant_urls.append(variant_url)

            num_variants = len(variant_urls)
            for idx, variant_url in enumerate(variant_urls):
                lender_product_variant_progress = len(progress) * ' ' + ' [' + str(idx + 1).zfill(len(str(num_variants))) + '/' + str(num_variants) + ']'
                self.log.d(lender_product_variant_progress + ' Fetching ' + variant_url)

                # visit each variant
                products_list.append(self.product_variant(variant_url))

        # if no variants, then just scrape for single product
        else:
            products_list.append(self.product_variant(url))

        return products_list

    def product_variant(self, url):

        object = {}
        # attach url for easy reference in the output
        object['Url'] = url

        response = requests.get(url)
        souped_response = BeautifulSoup(response.content, 'html.parser')

        try:
            details = souped_response.find('div', class_=re.compile('defaultInfobox'))

            try:
                object['Name'] = details.find('table').find('tr').find('th', text='Product Name').parent.find('td').text
            except Exception:
                pass

            try:
                # interest_rate_index = details.find('table').find_all('tr')
                object['Rate Type'] = details.find('table').find('th', text='Interest Rate Type').parent.find('td').text
            except Exception:
                object['Rate Type'] = 'N/A'

            try:
                object['Min Loan Amount'] = details.find('table').find('th', text='Minimum Loan Amount').parent.find('td').text
            except Exception:
                object['Min Loan Amount'] = 'N/A'

            try:
                object['Max Loan Amount'] = details.find('table').find('th', text='Maximum Loan Amount').parent.find('td').text
            except Exception:
                object['Max Loan Amount'] = 'N/A'

            try:
                object['Min Loan Term'] = details.find('table').find('th', text='Minimum Loan Term').parent.find('td').text
            except Exception:
                object['Min Loan Term'] = 'N/A'

            try:
                object['Max Loan Term'] = details.find('table').find('th', text='Maximum Loan Term').parent.find('td').text
            except Exception:
                object['Max Loan Term'] = 'N/A'

            try:
                object['Mortgage Offset Account'] = details.find('table').find('th', text='Mortgage Offset Account').parent.find('td').text
            except Exception:
                object['Mortgage Offset Account'] = 'N/A'

            try:
                object['Loan Redraw Facility'] = details.find('table').find('th', text='Loan Redraw Facility').parent.find('td').text
            except Exception:
                object['Loan Redraw Facility'] = 'N/A'

            try:
                object['Split Loan Facility'] = details.find('table').find('th', text='Split Loan Facility').parent.find('td').text
            except Exception:
                object['Split Loan Facility'] = 'N/A'

            try:
                object['Fixed Interest Option'] = details.find('table').find('th', text='Fixed Interest Option').parent.find('td').text
            except Exception:
                object['Fixed Interest Option'] = 'N/A'

            try:
                object['Suitable for Investment'] = details.find('table').find('th', text='Suitable for Investment').parent.find('td').text
            except Exception:
                object['Suitable for Investment'] = 'N/A'

            try:
                object['Extra Repayment'] = details.find('table').find('th', text='Extra Repayment').parent.find('td').text
            except Exception:
                object['Extra Repayment'] = 'N/A'

            try:
                object['Available as equity loan/line of credit'] = details.find('table').find('th', text='Available as equity loan/line of credit').parent.find('td').text
            except Exception:
                object['Available as equity loan/line of credit'] = 'N/A'

            try:
                object['Repayment Type'] = details.find('table').find('th', text='Repayment Type').parent.find('td').text
            except Exception:
                object['Repayment Type'] = 'N/A'

        except Exception:
            # if it fails here, return what we have so that we at least know this product exists,
            pass

        try:
            variant_id = url.split('#')[1]
            try:
                object['Variant'] = souped_response.find('div', class_=re.compile('productVariantTable')).find('tbody').find('tr', {'data-product-id':variant_id}).find('td', class_=re.compile('title')).text
            except Exception:
                object['Variant'] = 'N/A'

            try:
                object['Interest Rate'] = souped_response.find('div', class_=re.compile('productVariantTable')).find('tbody').find('tr', {'data-product-id':variant_id}).find('td', class_=re.compile('interest-rate')).find('span').text
            except Exception:
                object['Interest Rate'] = 'N/A'

            try:
                object['Comparison Rate'] = souped_response.find('div', class_=re.compile('productVariantTable')).find('tbody').find('tr', {'data-product-id':variant_id}).find('td', class_=re.compile('interest-rate')).find('div', class_='variant-comp-rate').find('span').text
            except Exception:
                object['Comparison Rate'] = 'N/A'

            try:
                max_insured_lvr_index = souped_response.find('div', class_=re.compile('productVariantTable')).find('thead').find('tr').index(souped_response.find('div', class_=re.compile('productVariantTable')).find('thead').find('tr').find('th', text=re.compile('Max Insured LVR')))
                object['Max Insured LVR'] = souped_response.find('div', class_=re.compile('productVariantTable')).find('tbody').find('tr', {'data-product-id':variant_id}).find_all('td')[max_insured_lvr_index].text
            except Exception:
                object['Max Insured LVR'] = 'N/A'

            try:
                max_insured_lvr_index = souped_response.find('div', class_=re.compile('productVariantTable')).find('thead').find('tr').index(souped_response.find('div', class_=re.compile('productVariantTable')).find('thead').find('tr').find('th', text=re.compile('Max LVR')))
                object['Max LVR'] = souped_response.find('div', class_=re.compile('productVariantTable')).find('tbody').find('tr', {'data-product-id':variant_id}).find_all('td')[max_insured_lvr_index].text
            except Exception:
                object['Max LVR'] = 'N/A'

        except Exception:
            # no variants
            pass

        return object
