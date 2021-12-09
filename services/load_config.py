import yaml
from typing import Dict

from load_logger import logging

try:
	CFG = yaml.safe_load(open("../config.yml", "r"))
except Exception as e:
	logging.error(f"Invalid config file! {e}")
	CFG = yaml.safe_load(open(".defaults.yml", "r"))
