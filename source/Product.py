class Product:

    def __init__(self, source, product_url, base_product_name=None):
        self._source = source
        self._product_url = product_url
        self._base_product_name = base_product_name
        self._product_information = None

    def as_dictionary(self):
        product = {}

        product['source'] = self._source.name()
        product['url'] = self.url()
        product['name'] = self.name()
        product['base_name'] = self.base_name()
        product['comparison_rate'] = self.comparison_rate()
        product['interest_rate'] = self.interest_rate()
        product['rate_type'] = self.rate_type()
        product['minimum_loan_amount'] = self.minimum_loan_amount()
        product['maximum_loan_amount'] = self.maximum_loan_amount()
        product['minimum_LVR'] = self.minimum_LVR()
        product['maximum_LVR'] = self.maximum_LVR()
        product['loan_purpose'] = self.loan_purpose()
        product['repayment_type'] = self.repayment_type()
        product['repayment_frequency'] = self.repayment_frequency()
        product['line_of_credit'] = self.line_of_credit()
        product['mortgage_offset_account'] = self.mortgage_offset_account()
        product['split_loan_facility'] = self.split_loan_facility()
        product['loan_redraw_facility'] = self.loan_redraw_facility()
        product['extra_repayments'] = self.extra_repayments()
        product['application_fee'] = self.application_fee()
        product['lenders_legal_fee'] = self.lenders_legal_fee()
        product['valuation_fee'] = self.valuation_fee()
        product['ongoing_fees'] = self.ongoing_fees()
        product['settlement_fee'] = self.settlement_fee()
        product['discharge_fee'] = self.discharge_fee()

        return product

    def _prepare_information(self):
        if self._product_information == None:
            self._product_information = self._source.product_information(self._product_url)

    def url(self):
        return self._product_url


    def name(self):
        self._prepare_information()
        return self._product_information['name'] if 'name' in self._product_information else ''
        

    def base_name(self):
        return self._base_product_name
        

    def comparison_rate(self):
        self._prepare_information()
        return self._product_information['Name'] if 'Name' in self._product_information else ''
        

    def interest_rate(self):
        self._prepare_information()
        return self._product_information['Name'] if 'Name' in self._product_information else ''
        

    def rate_type(self):
        self._prepare_information()
        return self._product_information['Rate Type'] if 'Rate Type' in self._product_information else ''
        

    def minimum_loan_amount(self):
        self._prepare_information()
        return self._product_information['Name'] if 'Name' in self._product_information else ''
        

    def maximum_loan_amount(self):
        self._prepare_information()
        return self._product_information['Name'] if 'Name' in self._product_information else ''
        

    def minimum_LVR(self):
        self._prepare_information()
        return self._product_information['Name'] if 'Name' in self._product_information else ''
        

    def maximum_LVR(self):
        self._prepare_information()
        return self._product_information['Name'] if 'Name' in self._product_information else ''
        

    def loan_purpose(self):
        self._prepare_information()
        return self._product_information['Name'] if 'Name' in self._product_information else ''
        

    def repayment_type(self):
        self._prepare_information()
        return self._product_information['Name'] if 'Name' in self._product_information else ''
        

    def repayment_frequency(self):
        self._prepare_information()
        return self._product_information['Name'] if 'Name' in self._product_information else ''
        

    def line_of_credit(self):
        self._prepare_information()
        return self._product_information['Name'] if 'Name' in self._product_information else ''
        

    def mortgage_offset_account(self):
        self._prepare_information()
        return self._product_information['Name'] if 'Name' in self._product_information else ''
        

    def split_loan_facility(self):
        self._prepare_information()
        return self._product_information['Name'] if 'Name' in self._product_information else ''
        

    def loan_redraw_facility(self):
        self._prepare_information()
        return self._product_information['Name'] if 'Name' in self._product_information else ''
        

    def extra_repayments(self):
        self._prepare_information()
        return self._product_information['Name'] if 'Name' in self._product_information else ''
        

    def application_fee(self):
        self._prepare_information()
        return self._product_information['Name'] if 'Name' in self._product_information else ''
        

    def lenders_legal_fee(self):
        self._prepare_information()
        return self._product_information['Name'] if 'Name' in self._product_information else ''
        

    def valuation_fee(self):
        self._prepare_information()
        return self._product_information['Name'] if 'Name' in self._product_information else ''
        

    def ongoing_fees(self):
        self._prepare_information()
        return self._product_information['Name'] if 'Name' in self._product_information else ''
        

    def settlement_fee(self):
        self._prepare_information()
        return self._product_information['Name'] if 'Name' in self._product_information else ''
        

    def discharge_fee(self):
        self._prepare_information()
        return self._product_information['Name'] if 'Name' in self._product_information else ''
        
