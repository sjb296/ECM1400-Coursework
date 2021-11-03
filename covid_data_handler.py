from typing import List, Dict, Tuple

def parse_csv_data(csv_filename: str) -> List[str]:
	"""
	Return a list of strings each containing a row of the csv.
	"""
	with open(csv_filename, "r") as csv:
		return [i.strip("\n") for i in csv.readlines()]

def process_covid_csv_data(covid_csv_data: List[str]) -> Tuple[int]:
	"""
	Return the total COVID cases in the last 7 days, the current number of
	hospital cases, and the total deaths, given a list of rows of a csv
	in government format.
	"""
	header = covid_csv_data[0].split(",")
	metrics = header[4:]
	body = [i.split(",") for i in covid_csv_data[1:]]

	# Calculate the number of cases in the last 7 days.
	# TODO: how did he get that value? fix this?
	print([int(i[6]) for i in body[1:8]])
	cases_in_last_7_days = sum([int(i[6]) for i in body[1:8]])
	print(cases_in_last_7_days)

	# Retrieve the current number of hospital cases.
	current_hospital_cases = int(body[0][5])

	# Calculate the cumulative number of COVID deaths.
	total_deaths = int([i[4] for i in body if i[4]][0])

	return cases_in_last_7_days, current_hospital_cases, total_deaths
