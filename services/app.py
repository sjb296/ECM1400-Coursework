from typing import List, Dict, Tuple, BinaryIO, Callable
from uk_covid19 import Cov19API
from flask import Flask
from flask import request
from flask import render_template
from flask import Markup
from datetime import datetime
from markupsafe import escape
import sched
import time
# Local modules
import covid_data_handling as cdh
import covid_news_handling as cnh

# List of update structures to render to the UI.
global updates
updates = []
# Queue of scheduled event objects to consume on refresh.
global update_events
update_events = sched.scheduler(time.time, time.sleep)

app = Flask(__name__,
			static_folder="/home/sam/Coursework/ECM1400 Coursework/static",
			template_folder="/home/sam/Coursework/ECM1400 Coursework/templates")

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

	global updates
	updates = []

	with open("updates.csv", "r") as f:
		updates_csv = [i.split("¬") for i in f.readlines()]

	# Remove newlines
	for i in updates_csv:
		i[-1] = i[-1][:-1]

	# TODO: Dismantle this when implementing logging
	# TODO: Check time format is valid
	updates_csv = [i for i in updates_csv if len(i) == 5 \
										  and i[0] != "00:00" \
										  and i[1] \
										  and (i[3] == "True" \
										  	   or i[4] == "True")]

	# Fill updates with renderable structures
	for row in updates_csv:
		current_update = dict()
		current_update["time"] = row[0]
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

		# New update time in seconds
		t = datetime.strptime(current_update["time"], "%H:%M")
		current_update["time_secs"] = t.second + t.minute*60 + t.hour*3600

	#print(updates_csv)
	print(updates)

def add_update(update: Dict) -> None:
	"""
	"""
	with open("updates.csv", "r") as f:
		update_rows = f.readlines()
		print(update_rows)
	with open("updates.csv", "a+") as f:
		line = f"{update['time']}¬{update['title']}¬" + \
			   f"{update['repeat']}¬{update['data']}¬{update['news']}\n"
		if line not in update_rows:
			f.write(line)
	return line not in update_rows

def schedule_repeat_event(scheduler: sched.scheduler,
				   		  interval: float,
						  action: Callable,
						  actionargs: Tuple = ()) -> None:
	"""
	"""
	scheduler.enter(interval, 1, do_repeat_event,
					(scheduler, interval, action, actionargs))

def do_repeat_event(scheduler: sched.scheduler,
					interval: float,
					action: Callable,
					actionargs: Tuple = ()) -> None:
	"""
	"""
	action(*actionargs)
	scheduler.enter(interval, 1, do_repeat_event,
					(scheduler, interval, action, actionargs))

def schedule_covid_updates(update_interval: float,\
						   update_name: str,
						   update_repeat: bool) -> sched.scheduler:
	"""
	TODO when function finished
	"""
	# TODO Customise arguments with config
	global update_events
	if update_repeat:
		schedule_repeat_event(update_events,
							  update_interval,
							  execute_data_update,
							  ())

def update_news(update_interval: float,\
				update_name: str,
				update_repeat: bool) -> None:
	"""
	TODO when function finished
	"""
	# TODO Customise arguments with config
	global update_events
	if update_repeat:
		schedule_repeat_event(update_events,
							  update_interval,
							  execute_news_update,
							  ())

def execute_data_update() -> None:
	"""
	"""
	print("----\nDATA\n----")

def execute_news_update() -> None:
	"""
	"""
	print("----\nNEWS\n----")

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

	global updates
	global update_events

	# Data (temp)
	data = cdh.covid_API_request()

	is_new_update = False
	# Handle an update addition request if there is one
	if request.args.get("update"):
		is_new_update = True
		new_update = dict()
		new_update["time"]  = request.args.get("update")
		new_update["title"] = request.args.get("two")
		new_update_repeat   = request.args.get("repeat")
		new_update_data     = request.args.get("covid-data")
		new_update_news     = request.args.get("news")

		if new_update_repeat == "repeat":
			new_update["repeat"] = True
		else:
			new_update["repeat"] = False
		if new_update_data == "covid-data":
			new_update["data"] = True
		else:
			new_update["data"] = False
		if new_update_news == "news":
			new_update["news"] = True
		else:
			new_update["news"] = False

		new_update["content"] = f"Interval: {new_update['time']}<br/>" + \
								f"Repeat: {new_update['repeat']}<br/>" + \
								f"Update data: {new_update['data']}<br/>" + \
								f"Update news: {new_update['news']}<br/>"
		new_update["content"] = Markup(new_update["content"])

		# New update time in seconds
		t = datetime.strptime(new_update["time"], "%H:%M")
		new_update["time_secs"] = t.second + t.minute*60 + t.hour*3600

		update_not_dupe = add_update(new_update)
		if update_not_dupe:
			updates.append(new_update)

	# Handle an update removal request if there is one
	update_to_remove = request.args.get("update_item")
	if update_to_remove:
		remove_update_from_file(update_to_remove)

		updates = [i for i in updates if i["title"] != update_to_remove]
		setup_event_queue()

	# Load the updates from the file
	#load_updates_from_file()
	# Load updates into the queue
	if is_new_update:
		# Add the new update to the queue
		if new_update["data"] and update_not_dupe:
			schedule_repeat_event(update_events,
								  new_update["time_secs"],
								  execute_data_update,
								  ())
		if new_update["news"] and update_not_dupe:
			schedule_repeat_event(update_events,
								  new_update["time_secs"],
								  execute_news_update,
								  ())

	print(updates)
	print(len(update_events.queue))
	print(update_events.run(blocking=False))

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

@app.before_first_request
def setup_event_queue() -> None:
	"""
	"""
	global update_events
	update_events = sched.scheduler(time.time, time.sleep)
	load_updates_from_file()
	for update in updates:
		if update["data"]:
			schedule_repeat_event(update_events,
								  update["time_secs"],
								  execute_data_update,
								  ())
		if update["news"]:
			schedule_repeat_event(update_events,
								  update["time_secs"],
								  execute_news_update,
								  ())


if __name__ == "__main__":
	"""
	Main loop
	"""
	app.run()
