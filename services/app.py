from typing import List, Dict, Tuple, BinaryIO
from uk_covid19 import Cov19API
from flask import Flask
from flask import request
from flask import render_template
from flask import Markup
<<<<<<< HEAD
<<<<<<< HEAD
from datetime import datetime
from datetime import timedelta
=======
>>>>>>> parent of b32c054... Implemented the thumbnail image and repeat update scheduling.
=======
>>>>>>> parent of b32c054... Implemented the thumbnail image and repeat update scheduling.
from markupsafe import escape
import sched
import time
# Local modules
import covid_data_handling as cdh
import covid_news_handling as cnh

# List of update structures to render to the UI.
global updates
updates = []
<<<<<<< HEAD
<<<<<<< HEAD
# List of non-repeat update structures to render to the UI
global s_updates
s_updates = []
# Queue of scheduled event objects to consume on refresh.
=======
# List of scheduled event objects to cycle through on refresh.
>>>>>>> parent of b32c054... Implemented the thumbnail image and repeat update scheduling.
=======
# List of scheduled event objects to cycle through on refresh.
>>>>>>> parent of b32c054... Implemented the thumbnail image and repeat update scheduling.
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

def remove_single_update_from_file(s_update_item: str) -> None:
	"""
	"""
	f = open("single_updates.csv", "r")
	# Read in and remove entry
	s_updates_csv = [i.split("¬") for i in f.readlines()]
	s_updates_csv = [i for i in s_updates_csv if i[1] != s_update_item]

	# Write back
	s_updates_rows = []
	s_updates_text = ""
	for row in s_updates_csv:
		s_updates_rows.append("¬".join(row))
	s_updates_text = "".join(s_updates_rows)
	f.close()

	f = open("single_updates.csv", "w")
	f.write(s_updates_text)
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

	#print(updates_csv)
	print(updates)

<<<<<<< HEAD
<<<<<<< HEAD
def load_single_updates_from_file() -> None:
	"""
	"""
	current_utime = time.time()

	global s_updates
	s_updates = []

	with open("single_updates.csv", "r") as f:
		s_updates_csv = [i.split("¬") for i in f.readlines()]

	# Remove newlines
	for i in s_updates_csv:
		i[-1] = i[-1][:-1]

	# TODO: Dismantle this when implementing logging
	# TODO: Check time format is valid
	s_updates_csv = [i for i in s_updates_csv if len(i) == 4       \
										  and i[0] > current_utime \
										  and i[1]                 \
										  and (i[2] == "True"      \
										  	   or i[3] == "True")]

	# Fill s_updates with renderable structures
	for row in s_updates_csv:
		current_s_update = dict()

		# Get the time until the event is to be run
		future_utime = row[0]
		current_utime = datetime.now().timestamp()
		interval = future_utime - current_utime
		current_s_update["time"] = interval

		current_s_update["title"] = row[1]
		current_s_update["content"] = f"Time until update: {interval}<br/>" + \
									  f"Update data: {row[3]}<br/>" +       \
									  f"Update news: {row[4]}<br/>"
		current_s_update["content"] = Markup(current_s_update["content"])

		if row[2] == "True":
			current_s_update["data"] = True
		else:
			current_s_update["data"] = False
		if row[3] == "True":
			current_s_update["news"] = True
		else:
			current_s_update["news"] = False

		if current_s_update not in s_updates:
			s_updates.append(current_s_update)

	print(s_updates_csv)
	print(s_updates)

def add_repeat_update(update: Dict) -> None:
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

def add_single_update(s_update: Dict) -> None:
	"""
	"""
	with open("single_updates.csv", "r") as f:
		s_update_rows = f.readlines()
		print(s_update_rows)
	with open("single_updates.csv", "a") as f:
		line = f"{s_update['time']}¬{s_update['title']}¬" + \
			   f"{s_update['data']}¬{s_update['news']}\n"
		if line not in s_update_rows:
			f.write(line)
	return line not in s_update_rows

def schedule_single_event(scheduler: sched.scheduler,
						  interval: float,
						  update_name: str,
						  action: Callable,
						  actionargs: Tuple = ()) -> None:
	"""
	"""
	scheduler.enter(interval, 1, action, actionargs)
	remove_update_from_file(update_name)

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
=======
=======
>>>>>>> parent of b32c054... Implemented the thumbnail image and repeat update scheduling.
def add_update(update_time: str,
			   update_name: str,
			   update_repeat: bool,
			   update_data: bool,
			   update_news: bool) -> None:
<<<<<<< HEAD
>>>>>>> parent of b32c054... Implemented the thumbnail image and repeat update scheduling.
=======
>>>>>>> parent of b32c054... Implemented the thumbnail image and repeat update scheduling.
	"""
	"""
	with open("updates.csv", "a") as f:
		#
		f.write(f"{update_time}¬{update_name}¬" +
				f"{update_repeat}¬{update_data}¬{update_news}\n")

<<<<<<< HEAD
<<<<<<< HEAD
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
	else:
		schedule_single_event(update_events,
							  update_interval,
							  execute_data_update,
							  (),
							  update_name)

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
	else:
		schedule_single_event(update_events,
							  update_interval,
							  update_name,
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
=======
>>>>>>> parent of b32c054... Implemented the thumbnail image and repeat update scheduling.
=======
>>>>>>> parent of b32c054... Implemented the thumbnail image and repeat update scheduling.

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
	if request.args.get("update"):
		print(request.args)
		update_time   = request.args.get("update")
		update_name   = request.args.get("two")
		update_repeat = request.args.get("repeat")
		update_data   = request.args.get("covid-data")
		update_news   = request.args.get("news")

		if update_repeat == "repeat":
			print("REPEAT")
			update_repeat = True
		else:
<<<<<<< HEAD
<<<<<<< HEAD
			new_update["repeat"] = False
			# Correct time to the appropriate unix time in the future
			current_utime = datetime.now().timestamp()
			interval = datetime.strptime(new_update["time"], "%H:%M")
			future_utime = current_utime            \
						   + interval.second        \
						   + interval.minute * 60   \
						   + interval.hour   * 3600

			print(current_utime)
			print(future_utime)
			new_update["time"] = future_utime
		if new_update_data == "covid-data":
			new_update["data"] = True
=======
			update_repeat = False
		if update_data == "covid-data":
			update_data = True
>>>>>>> parent of b32c054... Implemented the thumbnail image and repeat update scheduling.
=======
			update_repeat = False
		if update_data == "covid-data":
			update_data = True
>>>>>>> parent of b32c054... Implemented the thumbnail image and repeat update scheduling.
		else:
			update_data = False
		if update_news == "news":
			update_news = True
		else:
<<<<<<< HEAD
<<<<<<< HEAD
			new_update["news"] = False

		new_update["content"] = f"Interval: {new_update['time']}<br/>" + \
								f"Repeat: {new_update['repeat']}<br/>" + \
								f"Update data: {new_update['data']}<br/>" + \
								f"Update news: {new_update['news']}<br/>"
		new_update["content"] = Markup(new_update["content"])

		# New update time in seconds
		if new_update["repeat"]:
			t = datetime.strptime(new_update["time"], "%H:%M")
			new_update["time_secs"] = t.second + t.minute*60 + t.hour*3600

		update_not_dupe = add_repeat_update(new_update)
		if update_not_dupe:
			updates.append(new_update)
=======
			update_news = False

=======
			update_news = False

>>>>>>> parent of b32c054... Implemented the thumbnail image and repeat update scheduling.
		add_update(update_time,
				   update_name,
				   update_repeat,
				   update_data,
				   update_news)
<<<<<<< HEAD
>>>>>>> parent of b32c054... Implemented the thumbnail image and repeat update scheduling.
=======
>>>>>>> parent of b32c054... Implemented the thumbnail image and repeat update scheduling.

	# Handle an update removal request if there is one
	update_to_remove = request.args.get("update_item")
	if update_to_remove:
		remove_update_from_file(update_to_remove)

		global updates
		updates = [i for i in updates if i["title"] != update_to_remove]

	# Load the updates from the file
<<<<<<< HEAD
<<<<<<< HEAD
	#load_updates_from_file()
	# Load updates into the queue
	if is_new_update:
		# Add the new update to the queue
		if new_update["repeat"]:
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
		else:
			if new_update["data"] and update_not_dupe:
				schedule_single_event(update_events,
									  new_update["time_secs"],
									  new_update["title"],
									  execute_news_update,
									  ())
			if new_update["news"] and update_not_dupe:
				schedule_single_event(update_events,
									  new_update["time_secs"],
									  new_update["title"],
									  execute_data_update,
									  ())

	print(updates)
	print(len(update_events.queue))
	print(update_events.run(blocking=False))
=======
	load_updates_from_file()
	# Consume the update queue
>>>>>>> parent of b32c054... Implemented the thumbnail image and repeat update scheduling.
=======
	load_updates_from_file()
	# Consume the update queue
>>>>>>> parent of b32c054... Implemented the thumbnail image and repeat update scheduling.

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
