class Product:

	def __init__(self, scraper, url, base_product_name=None):
		self._scraper = scraper
		self._url = url
		self._base_product_name = base_product_name
		self._product_information = None

	def fetch(self):
		self._product_information = self._scraper.product_information(self._url)

	def get(self, key):
		if self._product_information is None:
			self.fetch()
		if self._product_information is not None and key in self._product_information:
			return self._product_information.get(key)
		else:
			return None

	def to_dict(self):
		return {
			'Source':                   self._scraper.name,
			'Url':                      self._url,
			'Base Name':                self._base_product_name,
			'Name':                     self.name(),
			'Interest Rate':            self.interest_rate(),
			'Fixed Rate':               self.fixed_rate_type(),
			'Variable Rate':            self.variable_rate_type(),
			'Minimum Loan Amount':      self.minimum_loan_amount(),
	        'Maximum Loan Amount':      self.maximum_loan_amount(),
			'Minimum LVR':              self.minimum_lvr(),
			'Maximum LVR':              self.maximum_lvr(),
			'Owner Occupied':           self.owner_occupied(),
			'investment':               self.investment(),
			'Principal and Interest':   self.principal_and_interest(),
			'Interest Only':            self.interest_only(),
			'Weekly Repayments':        self.repayment_frequency_weekly(),
			'Fortnightly Repayments':   self.repayment_frequency_fortnightly(),
			'Monthly Repayments':       self.repayment_frequency_monthly(),
			'Line of Credit':           self.line_of_credit(),
			'Mortgage Offset Account':  self.mortgage_offset_account(),
			'Split Loan Facility':      self.split_loan_facility(),
			'Loan Redraw Facility':     self.loan_redraw_facility(),
			'Extra Repayments':         self.extra_repayment(),
			'Application Fee':          self.application_fees(),
			'Lenders Legal Fee':        self.legal_fees(),
			'Valuation Fee':            self.valuation_fees(),
			'Ongoing Fees':             self.ongoing_fees(),
			'Settlement Fees':          self.settlement_fees(),
			'Discharge Fees':           self.discharge_fees()
		}

	def name(self):
		return self.get("Name")

	def interest_rate(self):
		return self.get("Interest Rate")

	def fixed_rate_type(self):
		if self.get("Fixed Rate") is not None:
			return self.get("Fixed Rate")
		else:
			rate_type = self.get("Rate Type")
			if rate_type is not None:
				return "fixed" in rate_type.lower()
			else:
				return None

	def variable_rate_type(self):
		if self.get("Variable Rate") is not None:
			return self.get("Variable Rate")
		else:
			rate_type = self.get("Rate Type")
			if rate_type is not None:
				return "variable" in rate_type.lower()
			else:
				return None

	def minimum_loan_amount(self):
		return self.get("Minimum Loan Amount")

	def maximum_loan_amount(self):
		return self.get("Maximum Loan Amount")

	def minimum_lvr(self):
		return self.get("Minimum LVR")

	def maximum_lvr(self):
		return self.get("Maximum LVR")

	def owner_occupied(self):
		if self.get("Owner Occupied") is not None:
			return self.get("Owner Occupied")
		else:
			loan_purpose = self.get("Loan Purpose")
			if loan_purpose is not None:
				return "owner occupied" in loan_purpose.lower()
			else:
				return None

	def investment(self):
		if self.get("investment") is not None:
			return self.get("investment")
		else:
			loan_purpose = self.get("Loan Purpose")
			if loan_purpose is not None:
				return "investment" in loan_purpose.lower()
			else:
				return None

	def principal_and_interest(self):
		if self.get("Principal and Interest") is not None:
			return self.get("Principal and Interest")
		else:
			repayment_type = self.get("Repayment Type")
			repayment_type = repayment_type.replace("&", "and")
			if repayment_type is not None:
				return "principal and interest" in repayment_type.lower()
			else:
				return None

	def interest_only(self):
		if self.get("Interest Only") is not None:
			return self.get("Interest Only")
		else:
			repayment_type = self.get("Repayment Type")
			if repayment_type is not None:
				return "interest only" in repayment_type.lower()
			else:
				return None

	def repayment_frequency_weekly(self):
		repayment_frequency = self.get("Repayment Frequency")
		if repayment_frequency is not None:
			return "weekly" in repayment_frequency.lower()
		else:
			return None

	def repayment_frequency_fortnightly(self):
		repayment_frequency = self.get("Repayment Frequency")
		if repayment_frequency is not None:
			return "fortnightly" in repayment_frequency.lower()
		else:
			return None

	def repayment_frequency_monthly(self):
		repayment_frequency = self.get("Repayment Frequency")
		if repayment_frequency is not None:
			return "monthly" in repayment_frequency.lower()
		else:
			return None

	def line_of_credit(self):
		return self.get("Line of Credit")

	def mortgage_offset_account(self):
		return self.get("Mortgage Offset Account")

	def split_loan_facility(self):
		return self.get("Split Loan Facility")

	def loan_redraw_facility(self):
		return self.get("Loan Redraw Facility")

	def extra_repayment(self):
		return self.get("Extra Repayments")

	def application_fees(self):
		return self.get("Application Fees")

	def legal_fees(self):
		return self.get("Legal Fees")

	def valuation_fees(self):
		return self.get("Valuation Fees")

	def ongoing_fees(self):
		return self.get("Ongoing Fees")

	def settlement_fees(self):
		return self.get("Settlement Fees")

	def discharge_fees(self):
		return self.get("Discharge Fees")
