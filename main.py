from typing import List, Dict, Tuple
from uk_covid19 import Cov19API
import sched
import time
# Local modules
import covid_data_handler as cdh

def schedule_covid_updates(update_interval: float,\
						   update_name: str) -> sched.scheduler:
	"""
	TODO when function finished
	"""
	data_sched = sched.scheduler(time.time, time.sleep)
	# TODO Customise arguments with config
	print(f"{update_name}")
	data_sched.enter(update_interval, 1, cdh.covid_API_request)
	data_sched.run()

if __name__ == "__main__":
	"""
	Main loop
	"""
	print("Main loop")
	while True:
		schedule_covid_updates(2.0, "Test event")
