import pytest
import time
from shutil import copy2
from testfixtures import TempDirectory
from app import *

"""
def test_serve_bootstrap_css() -> None:
	assert serve_bootstrap_css()

def test_serve_jquery3_js() -> None:
	assert serve_jquery3_js()

def test_serve_popper_js() -> None:
	assert serve_popper_js()

def test_serve_bootstrap_js() -> None:
	assert serve_bootstrap_js()

def test_serve_image_html() -> None:
	assert serve_image_html()

def test_serve_favicon() -> None:
	assert serve_favicon()
"""

def test_remove_update_from_file() -> None:
	# Test the function can delete a single update
	with TempDirectory() as d:
		test_update_content = "12:00¬TESTING TESTING TESTING テスト¬True¬True¬True\n"
		# Write the test update
		d.write("updates.csv", test_update_content)
		# Delete the test update
		remove_update_from_file("TESTING TESTING TESTING テスト")
		with d.read("updates.csv") as f:
			assert (test_update_content not in f.split("\n"))

		# Test the function can delete all updates with the same name
		test_update_content = "12:00¬TESTING TESTING TESTING テスト¬True¬True¬True\n"
		# Write the test update
		d.write("updates.csv", test_update_content*2)
		# Delete the test update
		remove_update_from_file("TESTING TESTING TESTING テスト")
		with d.read("updates.csv") as f:
			assert (test_update_content not in f.split("\n"))

		# Test the function doesn't error when there's no matching item
		remove_update_from_file("TESTING TESTING TESTING テスト")

# TODO
"""
def test_load_updates_from_file() -> None:
	global updates
	updates = []
	# Copy away the updates file so testing can be done safely
	copy2("updates.csv", "updates.csv.bak")
	with open("updates.csv", "w") as f:
		f.write("00:01¬Test¬True¬True¬True\n")
	load_updates_from_file()
	print(updates)
	assert updates == [{
		"content": Markup("Interval: 00:01<br/>"
						  + "Repeat: True<br/>"
						  + "Update data: True<br/>"
						  + "Update news: True<br/>"),
		"data": True,
		"news": True,
		"repeat": True,
		"time": "00:01",
		"time_secs": 60,
		"title": "Test",
	}]
	# REVERSE CHANGES TO THE UPDATES FILE
	copy2("updates.csv.bak", "updates.csv")
"""

def test_add_update() -> None:
	# Copy away the updates file so testing can be done safely
	copy2("updates.csv", "updates.csv.bak")
	add_update({
		"time": "12:00",
		"title": "Test",
		"repeat": True,
		"data": True,
		"news": True
	})
	with open("updates.csv", "r") as f:
		assert (f.readlines()[0] == "12:00¬Test¬True¬True¬True\n")

	copy2("updates.csv.bak", "updates.csv")

def test_schedule_single_event() -> None:
	copy2("updates.csv", "updates.csv.bak")
	# Write a test update to the updates file
	test_update_content = "12:00¬Test¬True¬True¬True\n"
	with open("updates.csv", "w") as f:
		f.write(test_update_content)

	scheduler = sched.scheduler(time.time, time.sleep)
	schedule_single_event("Test",
						  scheduler,
						  1.0,
						  print,
						  ("Test"))

	# Test that there is now one event on the queue
	assert len(scheduler.queue) == 1
	with open("updates.csv", "r") as f:
		assert len(f.readlines()) == 0

	copy2("updates.csv.bak", "updates.csv")
