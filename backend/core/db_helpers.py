import requests
from core.config import settings


TICKETMASTER_CONSUMER_SECRET=settings.TICKETMASTER_CONSUMER_SECRET
TICKETMASTER_CONSUMER_KEY = settings.TICKETMASTER_CONSUMER_KEY
BASE_URL = "https://app.ticketmaster.com/discovery/v2/events.json"

def fetch_events(keyword: str, country: str = "CA", city: str = None, 
                 start: str = None, end: str = None, size: int = 50):
   params = {
        "apikey": TICKETMASTER_CONSUMER_KEY,
        "keyword": keyword,
        "countryCode": country,
        "size": size,
    }
   if city:
      params["city"] = city
   if start:
      params["startDateTime"] = start
   if end:
      params["endDateTime"] = end

   resp = requests.get(BASE_URL, params=params)
   resp.raise_for_status()
   
   data = resp.json()
   simplified_events = []
  
   for e in data.get("_embedded", {}).get("events", []):
      venue = e.get("_embedded", {}).get("venues", [{}])[0]
      images = [img.get("url") for img in e.get("images", []) if img.get("url")]

      simplified_events.append({
            "name": e.get("name"),
            "id": e.get("id"),
            "url": e.get("url"),
            "images": images,
            "start_date_sales": e.get("sales", {}).get("public", {}).get("startDateTime"),
            "end_date_sales": e.get("sales", {}).get("public", {}).get("endDateTime"),
            "start_date_event": e.get("dates", {}).get("start", {}).get("localDate"),
            "info": e.get("info"),
            "please_note": e.get("pleaseNote"),
            "venue": {
                "name": venue.get("name"),
                "city": venue.get("city", {}).get("name"),
                "state": venue.get("state", {}).get("name"),
                "state_code": venue.get("state", {}).get("stateCode"),
                "country": venue.get("country", {}).get("name"),
                "address": venue.get("address", {}).get("line1"),
                "postal_code": venue.get("postalCode"),
            }
        })

   return simplified_events


import json
from pathlib import Path

DATA_FILE = Path("core/events_data.json")

def save_events(events: list):
   try:
      DATA_FILE.write_text(json.dumps(events, indent=2))
      print(f"Saved {len(events)} events to {DATA_FILE}")
   except Exception as e:
      print(f"Error saving events: {e}")


def load_events() -> list:
   if DATA_FILE.exists():
      return json.loads(DATA_FILE.read_text())
   return []
