import logging
from load_config import CFG

if CFG["logging"]["level"] == "debug":
	level = logging.DEBUG
if CFG["logging"]["level"] == "info":
	level = logging.INFO
if CFG["logging"]["level"] == "warning":
	level = logging.WARNING
if CFG["logging"]["level"] == "error":
	level = logging.ERROR

logging.basicConfig(
	filename=CFG["logging"]["filename"],
	level=level,
	format="%(levelname)s: %(asctime)s %(message)s"
)
