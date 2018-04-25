import pytest

def mock_request(test_source):
	source_file_path = ''
	if test_source == 'A':
		source_file_path = 'tests/data/data_a.html'
	elif test_source == 'B':
		pass
	else:
		pass

	if source_file_path != '':
		file = open(source_file_path,'r')
		return file.read()
	else:
		return ''


def test_to_dict():
	pass