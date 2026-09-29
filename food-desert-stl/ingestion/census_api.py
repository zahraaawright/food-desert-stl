"""Pull income and population data by census tract from the Census ACS API.

Requires a CENSUS_API_KEY environment variable (free at api.census.gov).
"""
import os
import requests
import pandas as pd

API_KEY = os.environ["CENSUS_API_KEY"]
YEAR = 2023
STATE_FIPS = "29"       # Missouri
COUNTY_FIPS = "510"     # St. Louis City; add more counties as needed

VARIABLES = {
    "B19013_001E": "median_household_income",
    "B01003_001E": "total_population",
}


def main() -> pd.DataFrame:
    var_codes = ",".join(VARIABLES.keys())
    url = (
        f"https://api.census.gov/data/{YEAR}/acs/acs5"
        f"?get=NAME,{var_codes}&for=tract:*&in=state:{STATE_FIPS}+county:{COUNTY_FIPS}&key={API_KEY}"
    )
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    data = response.json()
    df = pd.DataFrame(data[1:], columns=data[0])
    df = df.rename(columns=VARIABLES)
    df.to_csv("raw_census.csv", index=False)
    return df


if __name__ == "__main__":
    main()
