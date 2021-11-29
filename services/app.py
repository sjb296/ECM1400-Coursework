from typing import List, Dict, Tuple, BinaryIO
from uk_covid19 import Cov19API
from flask import Flask
from flask import request
from flask import render_template
from datetime import datetime, timedelta
from markupsafe import escape
import json
import re
import sched
import time
# Local modules
import covid_data_handling as cdh
import covid_news_handling as cnh

# Global list of update intervals to scheudle on startup,
# and representative structures to render on the UI.
global update_events
global updates
update_events = []
updates = []

app = Flask(__name__, \
			static_folder="/home/sam/Coursework/ECM1400 Coursework/static", \
			template_folder="/home/sam/Coursework/ECM1400 Coursework/templates")

def schedule_covid_updates(update_interval: float, \
						   update_name: str) -> sched.scheduler:
	"""
	TODO when function finished
	"""
	data_sched = sched.scheduler(time.time, time.sleep)
	# TODO Customise arguments with config
	data_sched.enter(update_interval, 1, cdh.covid_API_request)
	return update_name, data_sched

def update_news(update_interval: float,\
				update_name: str) -> sched.scheduler:
	"""
	TODO when function finished
	"""
	news_sched = sched.scheduler(time.time, time.sleep)
	# TODO Customise arguments with config
	news_sched.enter(update_interval, 1, cnh.news_API_request)
	return update_name, news_sched

@app.route("/index_files/bootstrap.css")
def serve_bootstrap_css() -> "Response":
	"""
	Serve bootstrap.css.
	"""
	return app.send_static_file("index_files/bootstrap.css")

@app.route("/index_files/jquery-3.js")
def serve_jquery_3_js() -> "Response":
	"""
	Serve jquery-3.js.
	"""
	return app.send_static_file("index_files/jquery-3.js")

@app.route("/index_files/popper.js")
def serve_popper_js() -> "Response":
	"""
	Serve popper.js.
	"""
	return app.send_static_file("index_files/popper.js")

@app.route("/index_files/bootstrap.js")
def serve_bootstrap_js() -> "Response":
	"""
	Serve bootstrap.js.
	"""
	return app.send_static_file("index_files/bootstrap.js")

@app.route("/index_files/%20image.html")
def serve_image_html() -> "Response":
	"""
	Serve %20image.html.
	"""
	return app.send_static_file("index_files/%20image.html")

@app.route("/favicon.ico")
def serve_favicon() -> "Response":
	return app.send_static_file("favicon.ico")

def parse_updates() -> Tuple[List[Dict], List]:
	"""
	Parse the scheduled updates file and return a list of update
	data structures.
	"""

	with open("interval_updates.txt", "r") as f:
		updates_list = [i.split("¬") for i in f.readlines()]

	# Remove invalid updates
	updates_list = [i for i in updates_list if not i.is_empty() \
											   and i[0] != "00:00" \
											   and (i[3] or i[4])]

	for i in updates_list:
		i[2] = bool(i[1])
		i[3] = bool(i[1])
		i[1] = bool(i[1])

	print(update_events, updates, updates_list)
	return update_events, updates

@app.route("/")
@app.route("/index")
def serve_index(prev_data: Dict = None, \
				prev_news: Dict = None) -> str:
	"""
	Acquire the necessary data and render the dashboard template
	(the homepage).

	Parameters
	----------
	prev_data: Dict - The previously requested & processed COVID
	data. Provided if only news is updated, or neither are.

	prev_news: Dict - The previously requested & processed news
	data. Provided if only data is updated, or neither are.
	"""

	# Handle an update removal request if there is one
	update_to_remove = request.args.get("update_item")
	if update_to_remove:
		with open("interval_updates.txt", "w+") as f:
			updates_list = [i.split("¬") for i in f.readlines()]
			updates_list = [i for i in updates_list \
							if i[1] != update_to_remove]
			updates_lines = ["¬".join(i) for i in updates_list]
			f.writelines(updates_lines)

	# Data (temp)
	data = cdh.covid_API_request()

	# Handle a news article removal request if there is one
	article_to_remove = request.args.get("notif")
	if article_to_remove:
		with open("excluded_news.txt", "a") as f:
			f.write(f"{article_to_remove}\n")

	# News (temp)
	news = cnh.news_API_request()

	# Delete news that has been removed by the user
	with open("excluded_news.txt", "r") as f:
		ex_news = [i[:-1] for i in f.readlines()]
		news["articles"] = [i for i in news["articles"] if i["title"] not in ex_news]


	return render_template( \
		"index.html", \
		title="COVID-19 Dashboard", \
		location=data["location"], \
		local_7day_infections=data["local_7day_infections"], \
		nation_location=data["nation_location"], \
		national_7day_infections=data["national_7day_infections"],
		hospital_cases="Hospital cases: " + str(data["hospital_cases"]), \
		deaths_total="Deaths total: " + str(data["deaths_total"]), \
		# News headlines list (right)
		news_articles=news["articles"], \
		# Scheduled updates list (left)
		updates=updates \
	)

print(__name__)
if __name__ == "__main__":
	"""
	Main loop
	"""
	#update_events, updates = parse_updates()
	app.run()
