"""Pull grocery and dollar store locations from the Google Places API.

Run manually for now; Airflow will call this on a schedule once it's stable.
Requires a GOOGLE_PLACES_API_KEY environment variable.
"""
import os
import requests
import pandas as pd

API_KEY = os.environ["GOOGLE_PLACES_API_KEY"]
SEARCH_TERMS = ["grocery store", "dollar store", "supermarket"]
ST_LOUIS_CENTER = "38.6270,-90.1994"
RADIUS_METERS = 20000


def fetch_places(query: str) -> list[dict]:
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": f"{query} in St. Louis, MO",
        "location": ST_LOUIS_CENTER,
        "radius": RADIUS_METERS,
        "key": API_KEY,
    }
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    return response.json().get("results", [])


def main() -> pd.DataFrame:
    rows = []
    for term in SEARCH_TERMS:
        for place in fetch_places(term):
            rows.append({
                "name": place.get("name"),
                "category": term,
                "lat": place["geometry"]["location"]["lat"],
                "lng": place["geometry"]["location"]["lng"],
                "address": place.get("formatted_address"),
            })
    df = pd.DataFrame(rows).drop_duplicates(subset=["name", "lat", "lng"])
    df.to_csv("raw_places.csv", index=False)
    return df


if __name__ == "__main__":
    main()
