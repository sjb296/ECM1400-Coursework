from covid_data_handler import parse_csv_data
from covid_data_handler import process_covid_csv_data

def test_parse_csv_data():
	"""
	Test that parse_csv_data returns the correct number of rows when
	parsing nation_2021-10-28.csv.
	"""
	data = parse_csv_data("nation_2021-10-28.csv")
	assert len(data) == 639

def test_process_covid_csv_data():
	"""
	Test that process_covid_csv_data returns the correct values
	for the example file nation_2021-10-28.csv.
	"""
	cases_in_last_7_days, current_hospital_cases, total_deaths = \
	process_covid_csv_data(parse_csv_data("nation_2021-10-28.csv"))

	assert cases_in_last_7_days == 240_299
	assert current_hospital_cases == 7_019
	assert total_deaths == 141_544
