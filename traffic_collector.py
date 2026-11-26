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
DATABASE = "traffic.db"
logging.basicConfig(level=logging.INFO)
def fetch_traffic():
   records = []
    for road, (lat, lon) in LOCATIONS.items():
         params = {
            "key": API_KEY,
              "point": f"{lat},{lon}",
               "unit": "KMPH"
              }
           try:
         response = requests.get(
               TOMTOM_URL, params=params, timeout=30
               )
            response.raise_for_status()
 flow = response.json()["flowSegmentData"]
speed = flow["currentSpeed"]
            free_speed = flow["freeFlowSpeed"]
congestion = (
   (1 - speed / free_speed) * 100
    if free_speed > 0 else None
               )
records.append({
    "collection_time": datetime.now(timezone.utc).isoformat(),
    "location": road,
   "latitude": lat,
                "longitude": lon,
   "current_speed": speed,
                "free_flow_speed": free_speed, 
   "congestion_percentage": congestion,
    "confidence": flow["confidence"],
    "road_closure": flow["roadClosure"]
   })

            logging.info("%s collected", road)


        except (requests.RequestException, KeyError, ValueError) as error:

 logging.error("%s: %s", road, error)
 return records

def save_to_database(records):
    if not records:
        logging.warning("No records to save.")
  return
 with sqlite3.connect(DATABASE) as connection:
        connection.execute("""
         CREATE TABLE IF NOT EXISTS live_traffic (
         collection_time TEXT,
                location TEXT,
                latitude REAL,
                longitude REAL,
                current_speed REAL,
                 free_flow_speed REAL,
                congestion_percentage REAL,
                confidence REAL,
                road_closure INTEGER
            )
        """)
  connection.executemany("""
   INSERT INTO live_traffic VALUES (
   :collection_time, :location, :latitude,
     :longitude, :current_speed, :free_flow_speed,
      :congestion_percentage, :confidence, :road_closure
         )
        """, records)
  logging.info("%s records saved", len(records))
if __name__ == "__main__":
    traffic_records = fetch_traffic()
  save_to_database(traffic_records)
 logging.info("Traffic collection completed.")
