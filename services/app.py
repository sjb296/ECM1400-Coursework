from typing import List, Dict, Tuple, BinaryIO
from uk_covid19 import Cov19API
from flask import Flask
from flask import request
from flask import render_template
from flask import Markup
from markupsafe import escape
import sched
import time
# Local modules
import covid_data_handling as cdh
import covid_news_handling as cnh

# List of update structures to render to the UI.
global updates
updates = []
# List of scheduled event objects to cycle through on refresh.
global update_events
update_events = []

app = Flask(__name__, \
			static_folder="/home/sam/Coursework/ECM1400 Coursework/static", \
			template_folder="/home/sam/Coursework/ECM1400 Coursework/templates")

def schedule_covid_updates(update_interval: float,\
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

def remove_update_from_file(update_item: str) -> None:
	"""
	"""
	f = open("updates.csv", "r")
	# Read in and remove entry
	updates_csv = [i.split("¬") for i in f.readlines()]
	updates_csv = [i for i in updates_csv if i[1] != update_item]

	# Write back
	updates_rows = []
	updates_text = ""
	for row in updates_csv:
		updates_rows.append("¬".join(row))
	updates_text = "".join(updates_rows)
	f.close()

	f = open("updates.csv", "w")
	f.write(updates_text)
	f.close()


def load_updates_from_file() -> None:
	"""
	"""

	with open("updates.csv", "r") as f:
		updates_csv = [i.split("¬") for i in f.readlines()]

	# Remove newlines
	for i in updates_csv:
		i[-1] = i[-1][:-1]

	# TODO: Dismantle this when implementing logging
	updates_csv = [i for i in updates_csv if len(i) == 5 \
										  and i[0] != "00:00" \
										  and i[1] \
										  and (i[3] == "True" \
										  	   or i[4] == "True")]

	# Fill updates with renderable structures
	for row in updates_csv:
		current_update = dict()
		current_update["title"] = row[1]
		current_update["content"] = f"Interval: {row[0]}<br/>" + \
									f"Repeat: {row[2]}<br/>" + \
									f"Update data: {row[3]}<br/>" + \
									f"Update news: {row[4]}<br/>"
		current_update["content"] = Markup(current_update["content"])

		if row[2] == "True":
			current_update["repeat"] = True
		else:
			current_update["repeat"] = False
		if row[3] == "True":
			current_update["data"] = True
		else:
			current_update["data"] = False
		if row[4] == "True":
			current_update["news"] = True
		else:
			current_update["news"] = False

		if current_update not in updates:
			updates.append(current_update)

	print(updates_csv)
	print(updates)

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

	# Data (temp)
	data = cdh.covid_API_request()

	# Handle an update addition request if there is one
#	if request.args.get("update"):
#		print(request.args)
#		add_update(request.args)

	# Handle an update removal request if there is one
	update_to_remove = request.args.get("update_item")
	if update_to_remove:
		remove_update_from_file(update_to_remove)

		global updates
		updates = [i for i in updates if i["title"] != update_to_remove]

	# Load the updates from the file
	load_updates_from_file()
	# Consume the update queue

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
		# Scheduled updates list (left)
		updates=updates, \
		# News headlines list (right)
		news_articles=news["articles"] \
	)

if __name__ == "__main__":
	"""
	Main loop
	"""
	app.run()
