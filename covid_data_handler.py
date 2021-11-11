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
	local_7day_infections = sum([int(i[6]) for i in body[2:9]])

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

	return local_7day_infections, current_hospital_cases, deaths_total

def covid_API_request(location: str = "Exeter", \
					  location_type: str = "ltla") -> Dict:
	"""
	Retrieve relevant COVID-19 information using the API and return
	it in a dictionary.

	Parameters
	----------
	location: str - The location to retrieve data for

	location_type: str - The type of area to retrieve data for

	Returns
	----------
	A dictionary containing
	- location: str - The location for which the local data is requested.

	- local_7day_infections: int - The total local infections in the last 7
	days.

	- nation_location: str - The name of the "nation" for which the national
	data is requested

	- national_7day_infections: int - The total national infections in the last 7
	days.

	- hospital_cases: int - The current number of national hospital cases.

	- deaths_total: int - The total number of deaths in nation_location.

	"""
	# Get local data
	local_filters = [
		f"areaType={location_type}",
		f"areaName={location}"
	]
	local_structure = {
		"areaCode" : "areaCode",
		"areaName" : "areaName",
		"areaType" : "areaType",
		"date" : "date",
		"newCasesBySpecimenDate" : "newCasesBySpecimenDate"
	}
	local_api = Cov19API(filters=local_filters, structure=local_structure)

	# Process local data
	local_csv_data = local_api.get_csv()
	local_body = [i.split(",") for i in local_csv_data.split("\n")[1:-1]]

	# Calculate the number of cases in the last 7 days.
	local_7day_infections = sum([int(i[4]) for i in local_body[0:7]])

	# Get national data
	nat_filters = [
		"areaType=nation",
		"areaName=England"
	]
	nat_structure = {
		"areaType" : "areaType",
		"date" : "date",
		"cumDeaths28DaysByDeathDate" : "cumDeaths28DaysByDeathDate",
		#"cumDailyNsoDeathsByDeathDate" : "cumDailyNsoDeathsByDeathDate",
		"hospitalCases" : "hospitalCases",
		"newCasesBySpecimenDate" : "newCasesBySpecimenDate"
	}
	nat_api = Cov19API(filters=nat_filters, structure=nat_structure)

	# Process national data
	nat_csv_data = nat_api.get_csv()
	nat_body = [i.split(",") for i in nat_csv_data.split("\n")[1:-1]]

	# Calculate the number of cases in the last 7 days
	national_7day_infections = sum([int(i[4]) for i in nat_body[1:8]])

	# Get the number of hospital cases
	if nat_body[0][3]:
		hospital_cases = nat_body[0][3]
	else:
		# Data for latest day incomplete
		hospital_cases = nat_body[1][3]

	# Get the total number of culumative deaths
	deaths_total = nat_body[2][2]

	return {
		"location": location,
		"local_7day_infections": local_7day_infections,
		"nation_location": "England", # Change with config?
		"national_7day_infections": national_7day_infections,
		"hospital_cases": hospital_cases,
		"deaths_total": deaths_total
	}
