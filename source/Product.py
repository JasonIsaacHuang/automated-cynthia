class Product:

    def __init__(self, source, product_url, base_product_name=None):
        self._source = source
        self._product_url = product_url
        self._base_product_name = base_product_name
        self._product_information = None

    def as_dictionary(self):
        product = {}

        product['Source'] = self._source.name()
        product['Url'] = self.url()
        product['Name'] = self.name()
        product['Base Name'] = self.base_name()
        product['Comparison Rate'] = self.comparison_rate()
        product['Interest Rate'] = self.interest_rate()
        product['Rate Type'] = self.rate_type()
        product['Minimum Loan Amount'] = self.minimum_loan_amount()
        product['Maximum Loan Amount'] = self.maximum_loan_amount()
        product['Minimum LVR'] = self.minimum_LVR()
        product['Maximum LVR'] = self.maximum_LVR()
        product['Loan Purpose'] = self.loan_purpose()
        product['Repayment Type'] = self.repayment_type()
        product['Repayment Frequency'] = self.repayment_frequency()
        product['Line of Credit'] = self.line_of_credit()
        product['Mortgage Offset Account'] = self.mortgage_offset_account()
        product['Split Loan Facility'] = self.split_loan_facility()
        product['Loan Redraw Facility'] = self.loan_redraw_facility()
        product['Extra Repayments'] = self.extra_repayments()
        product['Application Fee'] = self.application_fee()
        product['Lenders Legal Fee'] = self.lenders_legal_fee()
        product['Valuation Fee'] = self.valuation_fee()
        product['Ongoing Fees'] = self.ongoing_fees()
        product['Settlement Fees'] = self.settlement_fees()
        product['Discharge Fees'] = self.discharge_fees()

        return product

    def is_valid(self):
        return self._source.is_valid_page(self._product_url)

    def _prepare_information(self):
        if self._product_information == None:
            self._product_information = self._source.product_information(self._product_url)

    def _get(self, key):
        if key in self._product_information:
            return self._product_information[key]
        else:
            return ''

    def url(self):
        return self._product_url


    def name(self):
        self._prepare_information()
        return self._get('Name')
        

    def base_name(self):
        return self._base_product_name
        

    def comparison_rate(self):
        self._prepare_information()
        return self._get('Comparison Rate')

        

    def interest_rate(self):
        self._prepare_information()
        return self._get('Interest Rate')
        

    def rate_type(self):
        self._prepare_information()
        return self._get('Rate Type')
        

    def minimum_loan_amount(self):
        self._prepare_information()
        return self._get('Minimum Loan Amount')
        

    def maximum_loan_amount(self):
        self._prepare_information()
        return self._get('Maximum Loan Amount')
        

    def minimum_LVR(self):
        self._prepare_information()
        return self._get('Minimum LVR')
        

    def maximum_LVR(self):
        self._prepare_information()
        return self._get('Maximum LVR')
        

    def loan_purpose(self):
        self._prepare_information()
        return self._get('Loan Purpose')
        

    def repayment_type(self):
        self._prepare_information()
        return self._get('Repayment Type')
        

    def repayment_frequency(self):
        self._prepare_information()
        return self._get('Repayment Frequency')
        

    def line_of_credit(self):
        self._prepare_information()
        return self._get('Line of Credit')
        

    def mortgage_offset_account(self):
        self._prepare_information()
        return self._get('Mortgage Offset Account')
        

    def split_loan_facility(self):
        self._prepare_information()
        return self._get('Split Loan Facility')
        

    def loan_redraw_facility(self):
        self._prepare_information()
        return self._get('Loan Redraw Facility')
        

    def extra_repayments(self):
        self._prepare_information()
        return self._get('Extra Repayments')
        

    def application_fee(self):
        self._prepare_information()
        return self._get('Application Fee')
        

    def lenders_legal_fee(self):
        self._prepare_information()
        return self._get('Lenders Legal Fee')
        

    def valuation_fee(self):
        self._prepare_information()
        return self._get('Valuation Fee')
        

    def ongoing_fees(self):
        self._prepare_information()
        return self._get('Ongoing Fees')
        

    def settlement_fees(self):
        self._prepare_information()
        return self._get('Settlement Fees')
        

    def discharge_fees(self):
        self._prepare_information()
        return self._get('Discharge Fees')
        
