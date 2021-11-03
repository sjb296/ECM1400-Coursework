from typing import List, Dict

def parse_csv_data(csv_filename: str) -> List[str]:
	"""
	Return a list of strings each containing a row of the csv.
	"""
	with open(csv_filename, "r") as csv:
		return [i.strip("\n") for i in csv.readlines()]
