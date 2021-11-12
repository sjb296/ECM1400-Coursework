from typing import List, Dict, Tuple
from newsapi import NewsApiClient
import sched
import time
import datetime
import json

def news_API_request(covid_terms: str \
						="Covid COVID-19 coronavirus") -> Dict:
	"""
	TODO when function finished
	"""
	with open("newsapikey", "r") as f:
		api_key = f.readlines()[0][:-1]
		api = NewsApiClient(api_key=api_key)

	dt_today = datetime.date.today()
	dt_week_ago = dt_today - datetime.timedelta(days=7)

	return api.get_top_headlines(q=covid_terms.lower())
