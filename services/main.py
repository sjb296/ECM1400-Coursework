from typing import List, Dict, Tuple
from uk_covid19 import Cov19API
from flask import Flask
from flask import request
from flask import render_template
import sched
import time
# Local modules
import covid_data_handling as cdh
import covid_news_handling as cnh

app = Flask("COVID Dashboard", \
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

@app.route("/index")
def index():
	return render_template("index.html")

@app.route("/index_files/bootstrap.css")
def bootstrap_css():
	return app.send_static_file("index_files/bootstrap.css")

@app.route("/index_files/jquery-3.js")
def jquery_3_js():
	return app.send_static_file("index_files/jquery-3.js")

@app.route("/index_files/popper.js")
def popper_js():
	return app.send_static_file("index_files/popper.js")

@app.route("/index_files/bootstrap.js")
def bootstrap_js():
	return app.send_static_file("index_files/bootstrap.js")

@app.route("/index_files/%20image.html")
def image_html():
	return app.send_static_file("index_files/%20image.html")

if __name__ == "__main__":
	"""
	Main loop
	"""

	app.run()


	#while True:
	#	schedule_covid_updates(2.0, "Data event")
	#	update_news(10.0, "News event")
