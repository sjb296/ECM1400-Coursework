from typing import List, Dict, Tuple
from uk_covid19 import Cov19API
from flask import Markup
import json
import sched
import time

from load_logger import logging
from load_config import CFG

def parse_csv_data(csv_filename: str) -> List[str]:
	"""Return a list of strings each containing a row of the csv.

	Parameters:
		csv_filename: str - The name of the csv to read from.

	Returns:
		A list of strings where each string is a row of the csv.

	Modifies global(s):
		None

	Modifies file(s):
		None
	"""
	with open(csv_filename, "r") as csv:
		return [i.strip("\n") for i in csv.readlines()]

def schedule_covid_updates(update_name: str,
						   update_interval: float) -> None:
	"""Dummy function for the spec's automated tests.
	This program has ended up such that this function in app.py
	can't be tested with pytest.
	"""
	pass

def process_covid_csv_data(covid_csv_data: List[str]) -> Tuple[int]:
	"""Return the total COVID cases in the last 7 days, the current number of
	hospital cases, and the total deaths, given a list of rows of a csv
	in specification format.

	Parameters:
		covid_csv_data: List[str] - A list of rows of a csv in specification
		COVID data format.

	Returns:
		A tuple containing

		 - The total number of infections in the last 7 days
		 - The current hospital cases
		 - The cumulative number of deaths


	Modifies global(s):
		None

	Modifies file(s):
		None
	"""
	header = covid_csv_data[0].split(",")
	metrics = header[4:]
	body = [i.split(",") for i in covid_csv_data[1:-1]]

	# Calculate the number of cases in the last 7 days.
	local_7day_infections = 0
	cnt = 0
	cnt_lim = 7
	if not body[0][6]:
		# Blank
		cnt += 2
		cnt_lim += 2
	else:
		# Not blank
		cnt += 1
		cnt_lim += 1
	for i in range(len(body)):
		if cnt < cnt_lim:
			if body[cnt][6]:
				print(body[cnt][6])
				local_7day_infections += int(body[cnt][6])
		cnt += 1

	# Retrieve the current number of hospital cases.
	try:
		current_hospital_cases = int([i[5] for i in body if i[5]][0])
	except IndexError:
		current_hospital_cases = None

	# Calculate the cumulative number of COVID deaths.
	try:
		deaths_total = int([i[4] for i in body if i[4]][0])
	except IndexError:
		deaths_total = None

	return local_7day_infections, current_hospital_cases, deaths_total

def covid_API_request(location: str = CFG["data"]["local_loc"], \
					  location_type: str = CFG["data"]["local_loc_type"]) -> Dict:
	"""
	Retrieve relevant COVID-19 information using the API and return
	it in a dictionary.

	Parameters:
		location: str - The location to retrieve data for

		location_type: str - The type of area to retrieve data for

	Returns:
		A dictionary containing

		- location: str - The location for which the local data is requested.

		- local_7day_infections: int - The total local infections in the last 7
		days.

		- nation_location: str - The name of the "nation" for which the national
		data is requested

		- national_7day_infections: int - The total national infections in the last 7
		days.

		- hospital_cases: int - The current number of national hospital cases.

		- deaths_total: int - The total number of deaths in the UK.


	Modifies global(s):
		None

	Modifies file(s):
		None
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
	try:
		local_csv_data = local_api.get_csv()
	except Exception as e:
		# TODO: Handle SSLError - Connection related! LOG IT
		logging.error(e)
		return {
			"location": Markup(
				"<span style='color:red'>Error in COVID API request! </span>" +
				"<span style='color:red'>Please check your Internet connection.</span>"
			),
			"local_7day_infections": "???",
			"nation_location": CFG["data"]["nat_loc"],
			"national_7day_infections": "???",
			"hospital_cases": "???",
			"deaths_total": "???"
		}

	if local_csv_data:
		local_body = [i.split(",") for i in local_csv_data.split("\n")[1:-1]]

		# Calculate the number of cases in the last 7 days.
		local_7day_infections = 0
		cnt = 0
		cnt_lim = 7
		for i in local_body:
			if not i[4]:
				cnt += 1
				cnt_lim += 1
		# Skip the most recent data point because it's incomplete
		cnt += 1
		cnt_lim += 1
		for i in range(len(local_body)):
			if cnt < cnt_lim:
				if local_body[cnt][4]:
					local_7day_infections += int(local_body[cnt][4])
			cnt += 1
	else:
		local_7day_infections = Markup(
			"<span style='color:red'>Error in local location config!</span>"
		)

	# Get national data
	nat_filters = [
		"areaType=nation",
		f"areaName={CFG['data']['nat_loc']}"
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
	if nat_csv_data:
		nat_body = [i.split(",") for i in nat_csv_data.split("\n")[1:-1]]

		# Calculate the number of cases in the last 7 days
		#national_7day_infections = sum([int(i[4]) for i in nat_body[1:8]])
		# TODO fix this number?
		national_7day_infections = 0
		for i in nat_body[1:8]:
			if i[4]:
				n = int(i[4])
				national_7day_infections += n
		# Calculate the number of cases in the last 7 days.
		nat_7day_infections = 0
		cnt = 0
		cnt_lim = 7
		for i in nat_body:
			if not i[4]:
				cnt += 1
				cnt_lim += 1
		# Skip the most recent data point because it's incomplete
		cnt += 1
		cnt_lim += 1

		for i in range(len(nat_body)):
			if cnt < cnt_lim:
				nat_7day_infections += int(nat_body[cnt][4])
			cnt += 1

		# Get the number of hospital cases
		if nat_body[0][3]:
			hospital_cases = int(nat_body[0][3])
		else:
			# Data for latest day incomplete
			hospital_cases = int(nat_body[1][3])

		# Get the total number of culumative deaths
		deaths_filters = [
			"areaType=overview",
		]
		deaths_structure = {
			"cumDeaths28DaysByDeathDate" : "cumDeaths28DaysByDeathDate",
		}
		deaths_api = Cov19API(filters=deaths_filters, structure=deaths_structure)
		deaths_csv_data = deaths_api.get_csv()
		deaths_body = [i.split(",") for i in deaths_csv_data.split("\n")[1:-1]]

		# Get the number of hospital cases
		if deaths_body[0][0]:
			deaths_total = int(deaths_body[0][0])
		else:
			# Data for latest day incomplete
			deaths_total = int(deaths_body[1][0])
	else:
		national_7day_infections = Markup(
			"<span style='color:red'>Error in national location config!</span>"
		)
		hospital_cases = "Error in national location config!"
		deaths_total = "Error in national location config!"

	res = {
		"location": location,
		"local_7day_infections": local_7day_infections,
		"nation_location": f"{CFG['data']['nat_loc']}",
		"national_7day_infections": national_7day_infections,
		"hospital_cases": hospital_cases,
		"deaths_total": deaths_total
	}
	return res
