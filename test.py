from covid_data_handler import parse_csv_data

def test_parse_csv_data():
	"""
	Test that parse_csv_data returns the correct number of rows when
	parsing nation_2021-10-28.csv.
	"""
	data = parse_csv_data("nation_2021-10-28.csv")
	assert len(data) == 639
