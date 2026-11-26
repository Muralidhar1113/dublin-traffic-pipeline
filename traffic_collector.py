import os
import requests
import sqlite3
import logging
from datetime import datetime, timezone
API_KEY = os.environ["TOMTOM_API_KEY"]
TOMTOM_URL = (
   "https://api.tomtom.com/traffic/services/"
  "4/flowSegmentData/absolute/10/json"
)
LOCATIONS = {
  "O'Connell Street": (53.3498, -6.2603),
  "Dame Street": (53.3445,-6.2672),
      "College Green": (53.3438, -6.2597),
      "Pearse Street": (53.3439, -6.2489),
   "St Stephen's Green": (53.3382, -6.2591)
}
