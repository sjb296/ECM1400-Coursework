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

def process_dash_csv_data(local_csv_data: List[str], \
						  national_csv_data: List[str]) -> Tuple:
	"""
	Return a tuple containing the information to be displayed on the
	dashboard interface, given rows of local and national data.

	Parameters
	----------
	- local_csv_data: List[str] - A list of lines of the csv containing the result
	of an API request for local data.

	- national_csv_data: List[str] - A list of lines of the csv containing the
	result of an API request for national data.

	Returns
	----------
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

	return location, local_7day_infections, nation_location, \
		   national_7day_infections, hospital_cases, deaths_total


def covid_API_request(location: str = "Exeter", \
					  location_type: str = "ltla") -> Dict:
	"""
	Retrieve relevant COVID-19 information using the API and return
	it in a dictionary.
	"""
	if location_type == "overview":
		filters = [
			"areaType=overview"
		]
		structure = {
			"areaType" : "areaType",
			"date" : "date",
			"cumDeaths28DaysByDeathDate" : "cumDeaths28DaysByDeathDate",
			#"cumDailyNsoDeathsByDeathDate" : "cumDailyNsoDeathsByDeathDate",
			"hospitalCases" : "hospitalCases",
			"newCasesBySpecimenDate" : "newCasesBySpecimenDate"
		}
	else:
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

	local_csv_data = api.get_csv()
	return csv_data
