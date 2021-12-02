from typing import List, Dict, Tuple
from newsapi import NewsApiClient
import sched
import time
import datetime
import json

def news_API_request(covid_terms: str \
						="Covid COVID-19 coronavirus") -> Dict:
	"""
	Request today's news articles containing the words
	in covid_terms, and return the result in a dictionary.

	Parameters
	----------
	covid_terms: str - The terms with which to query the API.
	"""
	with open("newsapikey", "r") as f:
		api_key = f.readlines()[0][:-1]
		api = NewsApiClient(api_key=api_key)

	searches_list = []
	covid_terms_arr = covid_terms.split(" ")

	for i in covid_terms_arr:
		searches_list.append(dict(api.get_top_headlines(q=i)))

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

	news = {
		"status": status,
		"totalResults": total_results,
		"articles": articles
	}

	return news
