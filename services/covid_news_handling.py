from typing import List, Dict, Tuple
from newsapi import NewsApiClient
from flask import Markup
import sched
import time
import datetime
import logging

from load_config import CFG

def update_news(update_name: str) -> None:
	"""Dummy function for the automated tests. The real function is
	in app.py.
	"""
	pass

def news_API_request(covid_terms: str = CFG["news"]["covid_terms"]) -> Dict:
	"""
	Request today's news articles containing the words
	in covid_terms, and return the result in a dictionary.

	Parameters
	----------
	covid_terms: str - The terms with which to query the API.

	Returns
	-------
	news: Dict - A dictionary containing the results of the request to the
	news API.
	"""
	api_key = CFG["news"]["api_key"]
	api = NewsApiClient(api_key=api_key)

	searches_list = []
	covid_terms_arr = covid_terms.split(" ")

	try:
		for i in covid_terms_arr:
			searches_list.append(dict(api.get_top_headlines(q=i)))
	except Exception as e:
		print(e)
		return {"articles": [
			{
				"title": Markup("<span style='color:red;font-size:32pt'>"
								+ "Error: No connection!</span>"),
			 	"content": ""
			}
		]}

	all_ok = True
	status = "ok"
	for i in searches_list:
		if i["status"] != "ok":
			print(f"NEWS API STATUS {i['status']}")
			status = i["status"]

	total_results = sum([i["totalResults"] for i in searches_list])

	articles_dupes = []
	for i in searches_list:
		articles_dupes.extend(i["articles"])

	# Remove duplicates
	articles = []
	[articles.append(i) for i in articles_dupes if i not in articles]

	# Add a hyperlink and fix articles with no text content.
	for i in articles:
		tmp = i["title"]
		i["title"] = Markup(f"<a href='{i['url']}'>{tmp}</a>")
		if i["content"] == None:
			i["content"] = "No text preview found!"
		else:
			i["content"] = Markup(i["content"])

	news = {
		"status": status,
		"totalResults": total_results,
		"articles": articles
	}

	return news
