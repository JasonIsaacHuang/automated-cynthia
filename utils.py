import re


currency_pattern = u"[$¢£¤¥֏؋৲৳৻૱௹฿៛\u20a0-\u20bd\ua838\ufdfc\ufe69\uff04\uffe0\uffe1\uffe5\uffe6]"


def parse_percent_string(percent_string):
	if '%' in percent_string:
		percent_string = percent_string.rstrip('%')
		return float(percent_string) / 100
	else:
		if percent_string < 1:
			# Assume that if the value is below 1, it is already in float form
			return percent_string
		else:
			return percent_string / 100


def parse_currency(currency_string):
	currency_string = re.sub(currency_pattern, '', currency_string)
	currency_string = currency_string.replace(',', '')
	return currency_string


def parse_yesno(yesno_string):
	yesno_string = yesno_string.lower().strip()
	if 'yes' in yesno_string:
		return True
	elif 'no' in yesno_string:
		return False
	else:
		return None
