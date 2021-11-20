from typing import List, Dict, Tuple
from newsapi import NewsApiClient
import sched
import time
import datetime
import json

def news_API_request(covid_terms: str \
						="Covid COVID-19 coronavirus"):
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

	news = dict(api.get_everything(q=covid_terms))
	return news
