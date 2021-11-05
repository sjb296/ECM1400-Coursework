from typing import List, Dict, Tuple
from uk_covid19 import Cov19API
import json

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
	print(header)
	metrics = header[4:]
	body = [i.split(",") for i in covid_csv_data[1:-1]]
	for i in body:
		print(i)

	# Calculate the number of cases in the last 7 days.
	cases_in_last_7_days = sum([int(i[6]) for i in body[2:9]])

	# Retrieve the current number of hospital cases.
	if body[0][5]:
		# There is data for hospital cases
		current_hospital_cases = int(body[0][5])
	else:
		current_hospital_cases = None

	# Calculate the cumulative number of COVID deaths.
	try:
		deaths_total = int([i[4] for i in body if i[4]][0])
	except IndexError:
		deaths_total = None

	return cases_in_last_7_days, current_hospital_cases, deaths_total

def covid_API_request(location: str = "Exeter", \
					  location_type: str = "ltla") -> Dict:
	"""
	Retrieve relevant COVID-19 information using the API and return
	it in a dictionary.
	"""
	filters = [
		f"areaType={location_type}",
		f"areaName={location}"
	]

	structure = {
		"areaCode" : "areaCode",
		"areaName" : "areaName",
		"areaType" : "areaType",
		"date" : "date",
		"cumDeaths28DaysByDeathDate" : "cumDeaths28DaysByDeathDate",
		#"cumDailyNsoDeathsByDeathDate" : "cumDailyNsoDeathsByDeathDate",
		"hospitalCases" : "hospitalCases",
		"newCasesBySpecimenDate" : "newCasesBySpecimenDate"
	}

	api = Cov19API(filters=filters, structure=structure)

	csv_data = api.get_csv()
	return csv_data
