from typing import List, Dict, Tuple
from uk_covid19 import Cov19API
from flask import Flask
from flask import request
from flask import render_template
from markupsafe import escape
import sched
import time
# Local modules
import covid_data_handling as cdh
import covid_news_handling as cnh

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
	print(f"{update_name}")
	data_sched.enter(update_interval, 1, cdh.covid_API_request)
	data_sched.run()

def update_news(update_interval: float,\
				update_name: str) -> sched.scheduler:
	"""
	TODO when function finished
	"""
	news_sched = sched.scheduler(time.time, time.sleep)
	# TODO Customise arguments with config
	print(f"{update_name}")
	news_sched.enter(update_interval, 1, cnh.news_API_request)
	news_sched.run()

@app.route("/index_files/bootstrap.css")
def serve_bootstrap_css() -> str:
	"""
	Serve bootstrap.css.
	"""
	return app.send_static_file("index_files/bootstrap.css")

@app.route("/index_files/jquery-3.js")
def serve_jquery_3_js() -> str:
	"""
	Serve jquery-3.js.
	"""
	return app.send_static_file("index_files/jquery-3.js")

@app.route("/index_files/popper.js")
def serve_popper_js() -> str:
	"""
	Serve popper.js.
	"""
	return app.send_static_file("index_files/popper.js")

@app.route("/index_files/bootstrap.js")
def serve_bootstrap_js() -> str:
	"""
	Serve bootstrap.js.
	"""
	return app.send_static_file("index_files/bootstrap.js")

@app.route("/index_files/%20image.html")
def serve_image_html() -> str:
	"""
	Serve %20image.html.
	"""
	return app.send_static_file("index_files/%20image.html")

@app.route("/")
@app.route("/index")
def serve_index() -> str:
	"""
	Acquire the necessary data and render the dashboard template
	(the homepage).
	"""
	data = cdh.covid_API_request()

	return render_template( \
		"index.html", \
		title="COVID-19 Dashboard", \
		location=data["location"], \
		local_7day_infections=data["local_7day_infections"], \
		nation_location=data["nation_location"], \
		national_7day_infections=data["national_7day_infections"],
		hospital_cases="Hospital cases: " + str(data["hospital_cases"]), \
		deaths_total="Deaths total: " + str(data["deaths_total"]) \
		# Scheduled updates list (left)
		# News headlines list (right)
	)

if __name__ == "__main__":
	"""
	Main loop
	"""

	app.run()


	#while True:
	#	schedule_covid_updates(2.0, "Data event")
	#	update_news(10.0, "News event")
