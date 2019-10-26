import pathlib
import json

import pandas as pd

_DATA_PATH = pathlib.Path(__file__).parent

REQUESTS_PATH = _DATA_PATH / 'requests_history.csv'
LOCATIONS_PATH = _DATA_PATH / 'locations_history.csv'
